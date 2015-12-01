from unittest2 import TestCase
import simplejson as json
import boto3
from moto import mock_s3
import permission_lambda


class PermissionLambdaTests(TestCase):
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
