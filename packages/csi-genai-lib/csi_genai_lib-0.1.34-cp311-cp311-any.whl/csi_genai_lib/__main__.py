# ##################################################################################################
#  Copyright (c) 2024.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  __main__.py                                                                          #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################


import os
import signal

# Make sure CSI_MODULE is set properly to ensure Common.init is initializing this package
mod = os.getenv("CSI_MODULE", None)
if __package__ and not mod:
    os.environ["CSI_MODULE"] = __package__.split('.')[-1]
elif __package__ and mod:
    if mod.split('.')[-1] != __package__.split('.')[-1]:
        print(f"[WARNING] CSI_MODULE != Package Name -> {mod.split('.')[-1]} != {__package__.split('.')[-1]}")
else:
    raise RuntimeError(f"__package__ is not set")

from csiMVP.Common.init import CFG, Hue as hue, prep_shutdown, post_status_message
post_status_message(stage="2.0", message="Starting up", status="yellow")
signal.signal(signal.SIGTERM, prep_shutdown)
