import unittest2
import random
import boto3
import permission_lambda


class QueueTests(unittest2.TestCase):

    def setUp(self):
        self.client = boto3.client('sqs')
        self.prefix = 'test-' + hex(random.randint(0, 2 ** 48))[2:] + '-'
        response = self.client.create_queue(QueueName=self.prefix + 'test_queue')
        self.queue_url = response["QueueUrl"]

    def tearDown(self):
        self.client.delete_queue(QueueUrl=self.queue_url)

    def test_foo(self):
        pass

    def test_set_permissions_with_nonexistent_label(self):
        pass

    def test_set_permissions_existing_label_throws_exception(self):
        pass

    def test_delete_permissions_actually_deletes(self):
        client = boto3.client('sqs')
        response = client.create_queue(QueueName='test_queue')
        queue_url = response["QueueUrl"]

        client.add_permission(QueueUrl=queue_url, Label="other_permission",
                              AWSAccountIds=['23'], Actions=['SendMessage'])
        client.add_permission(QueueUrl=queue_url, Label="test_permission",
                              AWSAccountIds=['42'], Actions=['*'])

        permission_lambda.delete_permissions(queue_url, "test_permission")

        permission_statements = self._get_permission_statements(client, queue_url)
        test_permissions = [statement['Sid'] for statement in permission_statements]
        self.assertEqual(test_permissions, ["other_permission"])

    def test_delete_permissions_handles_nonexisting_label(self):
        client = boto3.client('sqs')
        response = client.create_queue(QueueName='test_queue')
        queue_url = response["QueueUrl"]

        permission_lambda.delete_permissions(queue_url, "foobar")
