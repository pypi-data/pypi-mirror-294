# ##################################################################################################
#  Copyright (c) 2024.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  If used, attribution of open-source code is included where required by original author          #
#                                                                                                  #
#  Filename:  post_sqs.py                                                                          #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

import json
from os import environ
from datetime import datetime

from csiMVP.Common.init import gethostname
from csiMVP.Toolbox.sqs_init import get_queue, post2queue

mod_version = "0.2.0"
# mod_name must be an fnmatch with [f"caber:{m.lower()}*" for m in CFG.G["caberModuleContainerNames"].keys()]
mod_name = "caber:csi_genai_lib:object"
user_agent = mod_name + "-" + mod_version

# Event method must be GetObject... PutObject will be ignored unless there is a response with a versionId
event_method = "PutObject"


def object_post(user, url, host, bucket, object_key, length):
    queue_url = get_queue(name="S3eventQueue")
    # queue_url = (environ.get("S3_SQS_QUEUE") or
    #              CFG.D.get('Dependencies', {}).get('message-queue', {}).get('queues', {}).get("S3eventQueue"))

    if not queue_url:
        print("No SQS queue URL found in environment")
        return

    # sqs = boto3.client('sqs')

    # Setting eventType to 'cloudtrail' will force S3_Scanner to process it as if it were a cloudtrail event.
    # This is needed because we need the CORI inserted into the message but this library does not have the mappings
    # to do that.
    message = {
        "eventTime": datetime.now().isoformat(),
        "eventSource": mod_name,
        "eventVersion": mod_version,
        "eventName": event_method,
        "eventType": "ObjectScan",
        "userAgent": user_agent,
        "userIdentity": {
            "type": "csi.svcId",
            "userName": user,
        },
        "latency_ms": 2,
        "sourceIPAddress": host or gethostname(),
        "awsRegion": environ.get("AWS_DEFAULT_REGION"),
        "requestParameters": {
            "url": f"https://{bucket}.s3.amazonaws.com/{object_key}",
            "Host": f"{bucket}.s3.amazonaws.com",
            "bucketName": bucket,
            "key": object_key
        },
        "additionalEventData": {"bytesTransferredIn": length},
        "event.type": "ObjectScan",
        "event.time": datetime.now().isoformat(),
        "event.source.name": mod_name,
        "event.source.version": mod_version,
        "user.from.host.name": host or gethostname(),
        "user.ua": user_agent,
        "user.name": user,
        "user.type": "csi.svcId",
        "event.direction": "<",
        "event.method.name": event_method,
        "event.code": 200,  # response_code
        "event.latency": 200.0,  # latency_ms
        "object.bytes": length,
        "bucket.name": bucket,
        "object.name": object_key

    }

    response = post2queue(queue_url, message=json.dumps(message))
    # sqs.send_message(
    #     QueueUrl=queue_url,
    #     MessageBody=json.dumps(message)
    # )

    print(f"Message sent to SQS queue: {queue_url}:")
    print(json.dumps(message))
    print(f"MessageId: {response['MessageId']}")
    return
