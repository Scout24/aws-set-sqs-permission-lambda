from __future__ import print_function, division, absolute_import
from botocore.exceptions import ClientError
import boto3
import json


class AlreadyExistsException(Exception):
    """Exception class for throwing if Element already exists"""
    pass


def get_usofa_accountlist(bucketname):
    """ Return a list of Account IDs """
    usofa_data = _get_usofa_data(bucketname)
    return [account_data['id'] for account_data in usofa_data.values()]


def _get_usofa_data(bucketname):
    """ Get USofA data from Bucket
    Return dict
    """
    client = boto3.client('s3')
    result = client.get_object(Bucket=bucketname, Key='accounts.json')
    return json.loads(result['Body'].read().decode('utf-8'))


def delete_permissions(queue_url, label):
    """ Delete Permissions by label (Sid)
    Return: None
    """
    client = boto3.client('sqs')
    try:
        client.remove_permission(QueueUrl=queue_url, Label=label)
    except ClientError as e:
        if e.response['Error']['Code'] != 'InvalidParameterValue':
            raise
        # We are failing silently since the label, which we would like to delete, does not exist


def set_permissions(queue_url, label, permissionlist, accountidlist):
    """ Set given Permissions for all accounts of accountlist.
    Return: None
    """
    client = boto3.client('sqs')
    try:
        client.add_permission(QueueUrl=queue_url, Label=label,
                              AWSAccountIds=accountidlist, Actions=permissionlist)
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidParameterValue':
            raise AlreadyExistsException(e.response['Error']['Message'])
        raise


def update_sqs_permissions(event, context):
    """ Institute permission for all accountids in the USofA on sqs queue
    Deletes permission before re-adding if permission-set exists
    Return None
    """
    pass
