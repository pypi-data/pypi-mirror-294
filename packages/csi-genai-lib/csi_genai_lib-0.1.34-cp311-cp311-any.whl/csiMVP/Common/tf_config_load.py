
# ##################################################################################################
#  Copyright (c) 2022.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  If used, attribution of open-source code is included where required by original author          #
#                                                                                                  #
#  Filename:  tf_config_load.py                                                                    #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

"""
    Terraform put configurations for each dependent service in environment variables.
    Get what input there is and update the target deependency configuration.

    If the environment variable's value is:
         'DISABLED'      =>   This dependency is not configured to be used so skip the initialization and discovery.

    If the environment variable's value startswith '{' or '[{', then do a json.loads and update the configuration
    for the target with the contents.
"""


import os
from json import loads, JSONDecodeError
from requests import get as req_get
from requests.exceptions import ConnectionError, InvalidSchema


def update_from_terraform(cfg):
    # Becasue of cycles and 'after apply' problems in Terraform, sometimes it's not possible to set
    # CSI_DEPENDENCY_CONFIG.  If that's the case, the Terraform script must write the dependencyConfig
    # contents to a config file in the Caber's main bucket.  After merging configs, CFG in inity.py will
    # call this function to decode the dependency string.
    dep_envars = os.getenv("CSI_DEPENDENCY_CONFIG", cfg.get("GLOBAL", {}).pop("dependencyConfig", None))
    if dep_envars and cfg:
        try:
            dep_envars = loads(dep_envars)
        except JSONDecodeError as err:
            print(f"[WARNING] Error decoding environment variable 'CSI_DEPENDENCY_CONFIG'. Using bootstrap default config.\n{err}")
        else:
            for k, v in dep_envars.items():
                if k.lower() in ['kafka', 'zookeeper']:
                    k = 'kafka-zookeeper'

                tgt_name = v.get("hostname", k)
                try:
                    cfg.D["Dependencies"][k].update({"useTarget": tgt_name})
                    existing = cfg.D["Dependencies"][k]["targets"].get(tgt_name) or {}
                except AttributeError:
                    cfg["Dependencies"][k].update({"useTarget": tgt_name})
                    existing = cfg["Dependencies"][k]["targets"].get(tgt_name) or {}

                for vk in v.keys():
                    existing.update({vk: v[vk]})
                if "ipv4" not in existing.keys():
                    existing.update({"ipv4": None})    # Keep it empty so that it can be updated later in OpenSearch.

                scheme = existing.get('scheme', 'http')
                if "neo4j" in k.lower() and isinstance(scheme, str) and not scheme.startswith("http"):
                    if existing.get('scheme', 'http').count('s'):
                        scheme = "https"
                    else:
                        scheme = "http"

                urls = []
                if isinstance(existing.get("urls"), list) and existing["urls"]:
                    urls = existing.get("urls")
                elif isinstance(existing.get("url"), list) and existing["url"]:
                    urls = existing.get("url")
                elif isinstance(existing.get("url", 0), str) and existing["url"]:
                    urls = [existing["url"]]

                if existing.get('host_full'):
                    if '://' not in existing.get('host_full'):
                        urls.append(f"{scheme}://{existing.get('host_full')}")
                    else:
                        urls.append(existing.get('host_full'))

                # Check if the hostname is that of an AWS EC2 instance.  If so, send a request to it to see if the
                # dependency is running on the same host.  If it responds on the right port
                # add the hostname to the URLs.
                envhost = os.getenv("HOSTNAME", "")
                if envhost.startswith("ip-") and envhost.endswith("compute.internal") and existing.get("port", False):
                    new_url = f"{scheme}://{os.getenv('HOSTNAME')}:{existing.get('port')}"
                    try:
                        req_get(new_url)
                    except InvalidSchema:
                        print(f"[DEBUG] Invalid schema {scheme} for {k}")
                    except ConnectionError:  # Must be from requests.exceptions
                        pass
                    else:
                        urls.append(new_url)

                existing.update({"urls": list(set(urls))})
                try:
                    cfg.D["Dependencies"][k]["targets"].update({tgt_name: existing})
                except AttributeError:
                    cfg["Dependencies"][k]["targets"].update({tgt_name: existing})
    return cfg
