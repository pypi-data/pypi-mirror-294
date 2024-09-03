# ##################################################################################################
#  Copyright (c) 2022.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  sqs_init.py                                                                          #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

import time
import boto3
from urllib.parse import urlsplit
from botocore.config import Config as boto3config
from botocore.exceptions import ClientError, EndpointConnectionError
from botocore.parsers import ResponseParserError

from csiMVP.Common.init import CFG
from csiMVP.Toolbox.retry import retry
from csiMVP.Toolbox.goodies import b_if_not_a
from csiMVP.Toolbox.aws_init import new_aws_resource

# ############# INCLUDE HERE THE NAMES OF TESTED MESSAGE QUEUE TYPES ################ #
#   These form the possible choices for:
#          CFG.D["Dependencies"]["message-queue"]["targets"][<host-name>]['type']
#
AWS_SQS_NAME = 'sqs.amazonaws.com'
SupportedMessageQueueTypes = [AWS_SQS_NAME, 'elastic-mq']
# ################################################################################### #


def check_sqs_config(on_err=False):

    target = CFG.D["Dependencies"]["message-queue"]["useTarget"]
    scfg = CFG.D["Dependencies"]["message-queue"]["targets"].get(target) or {}

    if check_sqs_name(target) == AWS_SQS_NAME:
        adv_config = boto3config(user_agent=CFG.user_agent,
                                 connect_timeout=10,
                                 read_timeout=5)
        mq_client = new_aws_resource('sqs', config=adv_config)
        scfg.update({"client": mq_client})

    if scfg is None:
        if not on_err:
            print(f"[WARNING] No message-queue config named '{CFG.D['Dependencies']['message-queue']['useTarget']}' was found")
            return None, None
        else:
            raise ValueError(f"No message-queue config named '{CFG.D['Dependencies']['message-queue']['useTarget']}' was found")
    else:
        return scfg, target


def check_sqs_name(name):
    sqslist = ['awssqs', 'sqs', 'sqsaws', 'amazonsqs', AWS_SQS_NAME]
    if isinstance(name, str) and name.lower() in sqslist or any([1 for x in sqslist if x in name.lower()]):
        return AWS_SQS_NAME
    else:
        return name


def _queue_object_from_client(mq_client, queue, op='get'):
    errs = []
    q_obj = None
    try:
        # Depending here on getting a 'QueueDoesNotExist' error.  Generating a random
        # queue name so we can avoid race conditions with other services doing the same check.
        if op == 'create':
            q_obj = mq_client.create_queue(QueueName=queue)
        else:
            q_obj = mq_client.get_queue_by_name(QueueName=queue)
    except EndpointConnectionError as err:
        # Here if the specified url point to a non-existent host
        errs.append(f"Failed to connect to message queue: {err}")
    except (ResponseParserError, ClientError) as err:
        # Elastic-MQ returns the below html when the queue does not exist and the boto3 SQS
        #      client spews "botocore.parsers.ResponseParserError: Unable to parse response"
        #      b'<!doctype html><title>404 Not Found</title><h1 style="text-align: center">
        #      404 Not Found</h1>'
        # AWS SQS throws a botocore Client Error with text "<title>404 Not Found"
        queue_not_found = ["<title>404 Not Found", "AWS.SimpleQueueService.NonExistentQueue"]
        if not any([err.args[0].count(m) for m in queue_not_found]):
            errs.append(f"Unknown error returned from message queue: {err}")
    finally:
        return q_obj, errs


# Returns client only if we can connect to the source_name and the bucket is in the source_name and configured
@retry(RuntimeError, total_tries=5, initial_wait=3, backoff_factor=1.75)
def _message_queue_create_client(on_err=False):
    # Step1: Get the message queue source configuration
    src_config, cfg_name = check_sqs_config(on_err=on_err)
    if src_config is None:
        return None

    host_type = src_config.get('type', '')
    if check_sqs_name(host_type.lower()) not in SupportedMessageQueueTypes:
        print(f"[CONFIG ERROR] In config 'CFG[GLOBAL][csiMessageQueue][{cfg_name}]': "
              f"Unsupported message queue type '{host_type}' ")
        src_config.update({'client': False})
        return None

    mq_client = src_config.get('client', None)

    # Step 2: Set up a new client for the message queue source if it has none
    if mq_client is None or mq_client == 'retry':
        if host_type.lower().startswith('elastic'):
            urls = b_if_not_a(src_config.get('url'), src_config.get('urls'))
            if urls is None:
                print(f"[CONFIG ERROR] No URL configured for Elastic-MQ host '{cfg_name}' ")
                src_config.update({'client': False})
                if on_err:
                    raise ValueError(f"No URL configured for Elastic-MQ host '{cfg_name}' ")
                else:
                    return None

            if isinstance(urls, str):
                urls = [urls]

            errs = []
            found = False
            for u in urls:
                try:
                    adv_config = boto3config(s3={'addressing_style': 'path'},
                                             user_agent=CFG.user_agent,
                                             user_agent_extra=None,
                                             connect_timeout=10,
                                             read_timeout=20)

                    mq_client = boto3.resource('sqs', endpoint_url=u,
                                               region_name='elasticmq',
                                               use_ssl=u.startswith('https'),
                                               aws_access_key_id=src_config.get('accessKey', ''),
                                               aws_secret_access_key=src_config.get('secretKey', ''),
                                               config=adv_config)
                except Exception as err:
                    errs.append(f"[WARNING] Failed to instantiate client for {host_type} host '{cfg_name}': {err}")
                    src_config.update({'client': False})
                else:
                    q, e = _queue_object_from_client(mq_client, CFG.new_id())
                    if not e:
                        found = True
                        src_config.update({'client': mq_client})
                        src_config.update({'url': u})
                        break

            if not found:
                if on_err:
                    raise RuntimeError(f"Cannot connect to any Elastic-MQ host in {urls}:\n{errs}")
                else:
                    print(f"Cannot connect to any Elastic-MQ host in {urls}:\n{errs}")
                    return None

    return mq_client


notification_bucket_policy = '{"Version": "2012-10-17", "Statement": [{"Sid": "AWSCloudTrailAclCheck20150319", "Effect": "Allow", "Principal": {"Service": "cloudtrail.amazonaws.com"}, "Action": "s3:GetBucketAcl", "Resource": "%bk_arn%"}, {"Sid": "AWSCloudTrailWrite20150319", "Effect": "Allow", "Principal": {"Service": "cloudtrail.amazonaws.com"}, "Action": "s3:PutObject", "Resource": "%ct_arn%", "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}}, {"Sid": "AWSLogDeliveryWrite", "Effect": "Allow", "Principal": {"Service": "delivery.logs.amazonaws.com"}, "Action": "s3:PutObject", "Resource": "%cw_arn%", "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}}, {"Sid": "AWSLogDeliveryAclCheck", "Effect": "Allow", "Principal": {"Service": "delivery.logs.amazonaws.com"}, "Action": "s3:GetBucketAcl", "Resource": "%bk_arn%"}]}'
notification_topic_policy = '{"Version": "2008-10-17", "Id": "__default_policy_ID", "Statement": [{"Sid": "__default_statement_ID", "Effect": "Allow", "Principal": {"AWS": "*"}, "Action": ["SNS:GetTopicAttributes", "SNS:SetTopicAttributes", "SNS:AddPermission", "SNS:RemovePermission", "SNS:DeleteTopic", "SNS:Subscribe", "SNS:ListSubscriptionsByTopic", "SNS:Publish", "SNS:Receive"], "Resource": "%topic_arn%", "Condition": {"StringEquals": {"AWS:SourceOwner": "%aws_id%"}}}, {"Sid": "AWSCloudTrailSNSPolicy20150319", "Effect": "Allow", "Principal": {"Service": "cloudtrail.amazonaws.com"}, "Action": "SNS:Publish", "Resource": "%topic_arn%"}]}'
event_queue_policy_sns = '{"Version": "2008-10-17", "Id": "__default_policy_ID", "Statement": [{"Sid": "__owner_statement", "Effect": "Allow"," Principal": {"AWS":"*"},"Action": "SQS:*", "Resource": "%queue_arn%"}, {"Sid": "topic-subscription-%topic_arn%", "Effect": "Allow", "Principal": {"AWS":"*"}, "Action": "SQS:*", "Resource": "%queue_arn%", "Condition": {"ArnLike": {"aws:SourceArn": "%topic_arn%"}}}]}'
event_queue_policy = '{"Version": "2008-10-17", "Id": "__default_policy_ID", "Statement": [{"Sid": "__owner_statement", "Effect": "Allow"," Principal": {"AWS":"*"},"Action": "SQS:*", "Resource": "%queue_arn%"}]}'


def get_queue_object_from_name(queue_name):

    if isinstance(queue_name, str) and queue_name:
        # If given a URL, the last element in the path is the queue name,
        # e.g., 'http://csi-dep-queue:9324/queue/csi-s3event-q'
        us = urlsplit(queue_name)
        queue_name = us.path.rsplit('/', 1)[-1]
    elif type(queue_name).__qualname__ == 'sqs.Queue':
        return queue_name  # In this case the argument queue_name is a Queue object, so return it

    queue_client = _message_queue_create_client()
    q_obj, err = _queue_object_from_client(queue_client, queue_name, op='get')

    if not q_obj and not err:
        q_obj, err = _queue_object_from_client(queue_client, queue_name, op='create')

    if err and isinstance(err, list):
        for e in err:
            print(e)

    return q_obj


def delete_queue(queue_name):
    qa = get_queue_object_from_name(queue_name)
    if qa:
        try:
            print(f"Deleting message queue '{qa.url}'")
            ret = qa.delete()
        except ClientError as err:
            ret = {'err': err}
        return ret
    else:
        return


def purge_queue(queue_name):
    qa = get_queue_object_from_name(queue_name)
    if qa:
        try:
            surl = urlsplit(qa.url)
            print(f"Purging message queue '{surl.path.split('/')[-1]}'")
            ret = qa.purge()
        except ClientError as err:
            ret = {'err': err}
        return ret
    else:
        return


def post2queue(queue_name, message=''):
    qa = get_queue_object_from_name(queue_name)
    if qa:
        try:
            sqs_resp = qa.send_message(MessageBody=message)
        except ClientError as err:
            sqs_resp = {'err': err}
        return sqs_resp
    else:
        return

def get_queue(name="APIshdwQueue"):
    q_name = CFG.D["Dependencies"]["message-queue"].get("queues", {}).get(name)
    if q_name is None:
        target = CFG.D["Dependencies"]["message-queue"].get("useTarget")
        q_name = CFG.D["Dependencies"]["message-queue"].get("targets", {})\
                                                       .get(target, {})\
                                                       .get('queues', {})\
                                                       .get(name)
    return  q_name
