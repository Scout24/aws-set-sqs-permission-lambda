from unittest2 import TestCase
from mock import patch
import simplejson as json
import boto3
from moto import mock_s3
import permission_lambda


class PermissionLambdaTests(TestCase):
    @mock_s3
    def test_get_usofa_account_ids_from_bucket(self):
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

        accountlist = permission_lambda.get_usofa_account_ids(bucketname)
        accountlist.sort()
        self.assertEqual(accountlist, ["123456789", "987654321"])

    @patch("permission_lambda.get_lambda_config_property")
    @patch("permission_lambda.get_usofa_account_ids")
    @patch("permission_lambda.delete_permissions")
    @patch("permission_lambda.set_permissions")
    def test_update_sqs_permissions(self,
                                    mock_set_permissions,
                                    mock_delete_permissions,
                                    mock_get_usofa_account_ids,
                                    mock_get_lambda_config_property):
        properties = {
            'usofa_bucket': "usofa_bucket",
            'label': 'test_label',
            'permissions': ["SendMessage"],
            'queue_url': "http://queue_url"
        }
        mock_get_lambda_config_property.return_value = properties
        mock_get_usofa_account_ids.return_value = ["1234", "42"]
        event = ""

        permission_lambda.update_sqs_permissions(event, properties['queue_url'])

        mock_set_permissions.assert_called_with(properties['queue_url'], properties['label'], properties['permissions'], mock_get_usofa_account_ids.return_value)
        mock_delete_permissions.assert_called_with(properties['queue_url'], properties['label'])
        mock_get_usofa_account_ids.assert_called_with(properties['usofa_bucket'])
