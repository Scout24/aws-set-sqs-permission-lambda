import boto3
import random
import simplejson as json
import unittest2
import time

import permission_lambda

class QueueTests(unittest2.TestCase):

    def setUp(self):
        self.client = boto3.client('sqs')
        self.prefix = 'test-' + hex(random.randint(0, 2 ** 48))[2:] + '-'
        response = self.client.create_queue(QueueName=self.prefix + 'test_queue')
        self.queue_url = response["QueueUrl"]
        self.account_id = self.queue_url.split("/")[3]

    def tearDown(self):
        self.client.delete_queue(QueueUrl=self.queue_url)

    def _get_permission_statements(self):
        """ Return a list of policy statements for given queue"""
        policy_response = self.client.get_queue_attributes(
            QueueUrl=self.queue_url, AttributeNames=['Policy'])
        policy = policy_response['Attributes']['Policy']
        return json.loads(policy)['Statement']

    def test_set_permissions_with_nonexistent_label(self):
        label = "test_label"
        expected_permissions = {
            'Action': 'SQS:*',
            'Effect': 'Allow',
            'Principal': {'AWS': self.account_id},
            'Sid': label}
        permission_lambda.set_permissions(self.queue_url, label, ["*"], [self.account_id])
        time.sleep(1)
        for statement in self._get_permission_statements():
            if statement["Sid"] == label:
                permission_result = statement

        permission_result.pop('Resource')
        self.assertEqual(expected_permissions, permission_result)

    def test_set_permissions_existing_label_throws_exception(self):
        label = "test_permission"
        self.client.add_permission(QueueUrl=self.queue_url, Label=label,
                                   AWSAccountIds=[self.account_id], Actions=['*'])
        time.sleep(2)
        self.assertRaises(permission_lambda.AlreadyExistsException,
                          permission_lambda.set_permissions,
                          self.queue_url, label, ["SendMessage"], [self.account_id])

    def test_delete_permissions_actually_deletes(self):
        self.client.add_permission(QueueUrl=self.queue_url, Label="other_permission",
                                   AWSAccountIds=[self.account_id], Actions=['SendMessage'])
        self.client.add_permission(QueueUrl=self.queue_url, Label="test_permission",
                                   AWSAccountIds=[self.account_id], Actions=['*'])

        permission_lambda.delete_permissions(self.queue_url, "test_permission")
        time.sleep(1)

        permission_statements = self._get_permission_statements()
        test_permissions = [statement['Sid'] for statement in permission_statements]
        self.assertEqual(test_permissions, ["other_permission"])

    def test_delete_permissions_handles_nonexisting_label(self):
        permission_lambda.delete_permissions(self.queue_url, "foobar")

if __name__ == "__main__":
    unittest2.main()
