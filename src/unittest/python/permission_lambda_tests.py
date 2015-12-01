from unittest2 import TestCase
import simplejson as json
import boto3
from moto import mock_s3
import permission_lambda


class PermissionLambdaTests(TestCase):
    def _get_permission_statements(self, client, queue_url):
        """ Return a list of policy statements for given queue"""
        policy_response = client.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=['Policy'])
        policy = policy_response['Attributes']['Policy']
        return json.loads(policy)['Statement']

    @mock_s3
    def test_get_usofa_accountlist_from_bucket(self):
        bucketname = "testbucket"
        usofa_data = {
            "account1": {
                "id": "123456789",
                "email": "user1@domain.invalid"
            },
            "account2": {
                "id": "987654321",
                "email": "user2@domain.invalid"
            }
        }

        client = boto3.client('s3')
        client.create_bucket(
            Bucket=bucketname,
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-west-1'
            })
        client.put_object(
            Bucket=bucketname,
            Key="accounts.json",
            Body=json.dumps(usofa_data)
        )

        accountlist = permission_lambda.get_usofa_accountlist(bucketname)
        accountlist.sort()
        self.assertEqual(accountlist, ["123456789", "987654321"])
