# ##################################################################################################
#  Copyright (c) 2023.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  If used, attribution of open-source code is included where required by original author          #
#                                                                                                  #
#  Filename:  supabase.py                                                                          #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

import requests
import os
from datetime import datetime


SUPABASE_URL = os.getenv("CSI_SUPABASE_URL")
SUPABASE_KEY = os.getenv("CSI_SUPABASE_API_KEY")
SUPABASE_LOGS_TABLE = os.getenv("CSI_DEPLOYMENT_LOGS_TABLE")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}


def post_status_to_supabase(log_data):
    if not SUPABASE_URL or not SUPABASE_KEY or not SUPABASE_LOGS_TABLE:
        print("Supabase environment variables not set. Skipping log post.")
        return False
    if not SUPABASE_URL.startswith("https://"):
        print("Supabase URL must start with https://. Skipping log post.")
        return False
    if not isinstance(log_data, dict):
        print("Log data must be a dictionary. Skipping log post.")
        return False

    # Force the timestamp to be UTC
    log_data["timestamp"] = datetime.utcnow().isoformat()

    must_have_keys = ["deployment_id", "stage", "category", "message", "group", "timestamp", "status"]
    good_keys = ["deployment_id", "stage", "category", "message", "group", "timestamp", "status", "progress_bar", "extra"]
    filtered_log_data = {k: v for k, v in log_data.items() if v and k in good_keys}

    check = set(must_have_keys).difference(set(filtered_log_data.keys()))

    if len(check):
        print(f"Log data missing the following keys: {check}.")

    try:
        # print(f"Sending the following to Supabase: {filtered_log_data}")
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/{SUPABASE_LOGS_TABLE}",
            headers=HEADERS,
            json=filtered_log_data
        )
    except Exception as e:
        print(f"Failed to post log. Exception: {e}")
        return False

    if response.status_code != 201:
        print(f"Failed to post log. Status Code: {response.status_code}. Response: {response.text}")
        return False

    return True
