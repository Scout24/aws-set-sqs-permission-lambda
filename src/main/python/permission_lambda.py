from __future__ import print_function, division, absolute_import
import boto3
import json


def get_usofa_accountlist(bucketname):
    """ Return a list of Account IDs """
    usofa_data = _get_usofa_data(bucketname)
    return [account_data['id'] for account_data in usofa_data.values()]


def _get_usofa_data(bucketname):
    """ Get USofA data from Bucket
    Return dict
    """
    conn = boto3.client('s3')
    result = conn.get_object(Bucket=bucketname, Key='accounts.json')
    return json.loads(result['Body'].read().decode('utf-8'))


def delete_permissions(queue_url, label):
    """ Delete Permissions by label (Sid)
    Return: None
    """
    pass


def set_permissions(queue_url, label, permissionlist, accountidlist):
    """ Set given Permissions for all accounts of accountlist.
    Return: None
    """
    pass


def update_sqs_permissions(event, context):
    """ Institute permission for all accountids in the USofA on sqs queue
    Deletes permission before re-adding if permission-set exists
    Return None
    """
    pass
