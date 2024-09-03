# ##################################################################################################
#  Copyright (c) 2022.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  json_encoder.py                                                                      #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

import json
import binascii
import base64
from datetime import datetime, timedelta

try:
    import pandas as pd
except ImportError:
    pd = None


class extEncoder(json.JSONEncoder):
    # Extend the json.JSONEncoder class to support datetime, bytes, and NaN, NaT, None, NA, etc.
    # by overloading the json method default.  This method cannot be used to convert sets to lists,
    # or dataframes to dicts, etc.
    # From the JSON docs:  https://docs.python.org/3/library/json.html
    #    ``default(obj)`` is a function that should return a serializable version
    #     of obj or raise TypeError. The default simply raises TypeError.
    def default(self, obj):
        # Match all the types you want to handle in your converter
        if isinstance(obj, timedelta):
            return obj.total_seconds() * 1000
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, bytes):
            try:
                obj = obj.decode('utf-8')
                return obj
            except UnicodeDecodeError as err:
                try:
                    obj = base64.b64encode(obj).decode('utf-8')
                    return obj
                except binascii.Error:
                    pass
        elif pd is not None and pd.isna(obj) and not isinstance(obj, (pd.DataFrame, pd.Series)):
            return None
        elif not isinstance(obj, (str, int, float, list, dict, bool)):
            try:
                return json.JSONEncoder.default(self, obj)
            except (ValueError, TypeError):
                return None

        # Call the default method for (str, int, float, list, dict, bool)
        return json.JSONEncoder.default(self, obj)
