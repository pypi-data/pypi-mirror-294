# ##################################################################################################
#  Copyright (c) 2022.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  __init__.py                                                                          #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

# __init__.py = Ensure the CSI_MODULE environment variable is correctly set to the current module
# name so that module specific initialization done in Common.init.CFG works.

import os

MODULE = "csi_genai_lib"
# if __package__:                         # This succeeds if the module is run with 'python -m ./Module_Name'
#     MODULE = __package__                # and the __init__.py file is in the directory ./Module_Name
# elif __file__.endswith('__init__.py'):  # This should be redundant and unnecessary but...
#     MODULE = __file__.split('/')[-2]
# else:
#     raise RuntimeWarning(f"[{MODULE}/__init__.py] Something went horribly wrong...")

if not os.getenv("CSI_MODULE"):
    os.environ["CSI_MODULE"] = MODULE


from .main import MainHandler
from .post_sqs import object_post
from .aws_init import S3C as s3client

__all__ = ['MainHandler', 'sqs_message', 'object_post', 's3client']

handler = MainHandler()
new_request = handler.new_request
update_response = handler.update_response
sqs_message = handler.sqs_message
