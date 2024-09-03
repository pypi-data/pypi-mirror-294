# ##################################################################################################
#  Copyright (c) 2022.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  goodies.py                                                                           #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

"""
A common location for a number of convenience functions
"""

from urllib.parse import urlsplit
from fnmatch import filter as fnfilter
from itertools import chain
import json
import re
import os
from socket import getfqdn
from collections import Counter
from ipaddress import ip_address, IPv4Address, IPv6Address, AddressValueError

from botocore.utils import is_valid_endpoint_url
from csiMVP.Toolbox.aws_init import check_s3_name, get_aws_regions, AWS_S3_NAME, AWS_S3_SHORT_NAME

try:
    from pandas import isna, DataFrame, Series
except ImportError:
    DataFrame = None
    Series = None
    isna = None


def normalize_host_config(scfg: dict, trgt, svc_domain='', auth=False, force=False):
    """
    Normalized one host configuration to a standard form.  Won't normalize if the configuration has already
    been normalized, or if it has a key enabled with value False, unless 'force' is set to True.

    Standard host configuration dictionaries may have the following keys and others:
    keys = {'scheme', 'host', 'port', 'accessKey', 'secretKey', 'use_ssl', 'is_up', 'enabled', 'normalized', 'key'
            'initialized', 'region', 'hostname', 'ipv4', 'ipv6', 'host_full', 'domain', 'serviceName', 'upstrm'}

    scheme is one of 'http', 'https', 'file', a custom scheme like 'bolt' for neo4j, or None

    :param svc_domain: The value of CFG.svc_domain, if available. Default is ''
    :param scfg: The input host configuration dictionary.
    :param trgt: The target host if caller of this function is iterating over a set of {target: {scfg} } dicts.
    :param auth: Should auth keys 'accessKey', 'secretKey', be used to build a URL with basic http auth.
    :param force:
    :return: normalized scfg dictionary.
    """

    norm = scfg.get("normalized", False)
    if not force and norm or not scfg.get("enabled", True):
        return scfg

    scfg = shp_to_port(scfg)
    scfg = _step1_norm_host_key(scfg, trgt, svc_domain=svc_domain)
    scfg = _step2_check_ssl(scfg)
    scfg = _step3_norm_scheme(scfg)
    scfg = _step4_norm_url_urls(scfg)

    if not scfg.get('host') or not scfg.get('host_full'):
        raise ValueError(f"Empty host! {scfg}")
    if ':' in scfg.get('host_full', ''):
        hf = scfg['host_full'].rsplit(':',1)[0]
        scfg.update({'host_full': hf})

    scfg.update({"normalized": True})
    return scfg


def most_common(lst: list):
    """
    Finds the most often occurring value in the input list that is not None or an empty string. or the first
    if no value occurs more than once.
    :param lst: List of values that may have duplicates.
    :return: The most often occurring value in the list
    """

    # Eliminate None and empty string values, then normalize remaining values as strings
    lst = [str(item) for item in lst if item is not None and item != '']
    # If the list is empty after filtering, return None
    if not lst:
        return None
    # Count occurrences of each value in the list
    counts = Counter(lst)
    # Find the most common value (returns a list of tuples (value, count))
    most_common_data = counts.most_common(1)
    # If the most common value has a count of 1, return the first value of the list
    if most_common_data[0][1] == 1:
        return lst[0]
    # Otherwise, return the most common value
    return most_common_data[0][0]


def is_ip_url(url, value_only=True):
    """
    If running on an EC2 instance the hostname can be something like
    'http://ip-10-0-0-220.us-west-1.compute.internal:9200'. If so, extract the Ipv4 address and return.

    :param url:
    :param value_only: return just the ip address if Ture.  Othersise, return dict of {'ipv4': ip}
    :return:
    """

    url = url.split('://')[-1]
    url = url.rsplit(':', 1)[0]
    ip_addr = check_ip_address(url, no_zero=True, value_only=value_only)
    if ip_addr:
        return ip_addr

    pattern = r'^(?:[a-z]{0,10}-?)(\d{1,3}[-|\.]\d{1,3}[-|\.]\d{1,3}[-|\.]\d{1,3})'
    match = re.search(pattern, url)

    if match:
        ip_addr = match.group(1).replace('-', '.')
        return check_ip_address(ip_addr, no_zero=True, value_only=value_only)

    return '' if value_only else {}


# If pandas is available use it to find if a value is a dataframe, series, or empty dataframe
def b_if_not_a(a, b):
    a_is_empty_df = False
    a_is_na = False
    if DataFrame is not None:
        a_is_empty_df = isinstance(a, (DataFrame, Series)) and a.empty
        a_is_na = isna(a)
    a_is_empty_other = not isinstance(a, (bool, int, float)) and not a
    if a_is_empty_df or a_is_na or a_is_empty_other:
        return b
    else:
        return a


def first_valid(*args, blank='evaluates_false', oftype=str):
    """
    Returns the first valid argument passed to the function where valid is determined by
    the parameters 'blank' and 'oftype'.  'blank' determines the method by which an argument A is deemed valid.

    When param 'blank' is:
        'evaluates_false': If the expression 'bool(A)' for arg A returns False, A is not valid.
        'is_none':         If the expression 'A is not None' for arg A returns False, A is not valid.
        None:              Same as 'is_none'
        <list>:            If oftype is not 'list', and if A is not in list 'blank', A is not valid
        <dict>:            If oftype is not 'dict', and if A is not in list 'blank.values()', A is not valid
        <function>:        A is valid if function(A) returns True

        If none of the above applies, then A is considered valid so long as A != 'blank'

    :param args: any number of arguments of any type
    :param blank: Can be one of the command strings 'evaluates_false' or 'is_none', a function that
                  returns True if valid, a list or dict of valid values. Default is 'evaluates_false'

    :param oftype: If set to a type, a in args is considered valid only if isinstance(a, type) is True
    :return: first valid arg or None
    """

    def _is_none(x):
        return x is None

    def _is_not_equal(x):
        if isinstance(x, type(blank)):
            return x != blank
        else:
            return True

    def _is_not_in(x):
        if isinstance(blank, list) and not isinstance(x, list):
            return x not in blank
        elif isinstance(blank, dict) and not isinstance(x, dict):
            return x not in list(blank.values())
        else:
            return _is_not_equal(x)

    if len(args) == 1 and isinstance(args[0], list):
        args = args[0]

    if isinstance(oftype, type):
        args = [a for a in args if isinstance(a, oftype)]

    if blank is None or (isinstance(blank, str) and blank.lower() == 'is_none'):
        out = filter(_is_none, args)
    elif isinstance(blank, str) and blank.lower() == 'evaluates_false':
        out = filter(None, args)
    elif isinstance(blank, type(_is_none)):
        # Here if 'blank' is a function
        # noinspection PyTypeChecker
        out = filter(blank, args)
    elif isinstance(blank, list) or isinstance(blank, dict):
        out = filter(_is_not_in, args)
    else:
        out = filter(_is_not_equal, args)

    out = list(out)
    if out:
        return out[0]
    else:
        return None


def _step2_check_ssl(out: dict) -> dict:
    if out.get("use_ssl", None) is None:
        if out.get("scheme", "") == 'https':
            out.update({"use_ssl": True})
        elif str(out.get("port", "")) == "443":
            out.update({"use_ssl": True})
        else:
            out.update({"use_ssl": False})
    return out


def _step4_norm_url_urls(d: dict) -> dict:
    utemp = []
    utemp.extend(shp_to_url(d, include_auth=False))

    if isinstance(d.get('url'), list):
        utemp.extend(d.pop('url', []))
    elif isinstance(d.get('url'), str):
        utemp.append(d.pop('url'))
    if isinstance(d.get('urls'), list):
        utemp.extend(d.pop('urls', []))
    elif isinstance(d.get('urls'), str):
        utemp.append(d.pop('urls'))

    utemp = [u for u in utemp if isinstance(u, str) and u]
    utemp.sort(key=len)

    mc_url = most_common(utemp)
    if mc_url:
        goodurls = [] if is_ip_url(mc_url) else [mc_url] if mc_url else []
        # Order such that longest non-ip URL is first.
        goodurls.extend(list(set([u for u in utemp if isinstance(u, str) and u and not is_ip_url(u) and u != mc_url])))
        goodurls.sort(key=len, reverse=True)
        goodurls.extend(list(set([u for u in utemp if isinstance(u, str) and u and is_ip_url(u)])))

        goodurls = [
            u for u in goodurls
            if not (
                u.endswith(os.getenv("CSI_ROLE_EXTERNAL_ID", "")) or
                u.endswith(os.getenv("CSI_TENANT_ID", "")) or
                u.endswith(os.getenv("CSI_DEPLOYMENT_ID", ""))
            )
        ]

        d.update({'urls': goodurls})

    else:
        d.update({'urls': []})

    return d


def _step3_norm_scheme(d: dict) -> dict:
    default_scheme = 'https' if str(d.get('port', 0)) == "443" or d.get('use_ssl', False) else 'http'
    scheme = first_valid(d.get('scheme'), d.get('protoForXFProto'), 
                         most_common([urlsplit(p).scheme for p in d.get('urls', [])
                                      if p and isinstance(d.get('urls'), list)]), default_scheme)
    if scheme:
        d.update({"scheme": scheme})
    return d


def _step1_norm_host_key(d: dict, key: str = '', svc_domain='') -> dict:
    """
    Every configured host has a standard dictionary of values. From this dictionary determine if
    the 'host' is an AWS service.  If so, then make sure the host and host_full keys in the host
    dictionary are standardized so their use will be consistent everywhere.

    If not an AWS service, the host configuration parameters can be specified in a number of ways.
    Through many iterations I found forcing a one-size-fits-all config for hosts was nearly
    impossible to maintain as new hosts types were added. So, instead this function allows flexibility
    by deconstructing every value related to the name of the host from the host config dictionary into
    schemes, prefixes, hostnames, instance numbers, domains, and ports.  Then it reconstructs the
    needed parameters from this base set.

    Priority is given to values explicitely stated.  For example if the key {"scheme": "http"}
    exists then it's prioritized over the scheme 'https' in {'urls': ['https://hostname']}.

    NOTE: On docker networks, a DNS lookup of the container name yields a valid result, but so does
    prefix-containerName-instance.  So do a lookup for the fully-qulaified domain name using the
    shortest valid values for containerName to find the FQDN.  If we have the FQDN and the container
    name then extract the prefix, instance, domain, etc.  Check against values specified in the
    host config dictionary.

    :param d:
    :return:
    """

    keys = {'scheme', 'host', 'port', 'accessKey', 'secretKey', 'use_ssl', 'is_up', 'url',
            'urls', 'enabled', 'normalized', 'key', 'initialized', 'region', 'hostname',
            'ipv4', 'ipv6', 'host_full', 'domain', 'serviceName', 'upstrm', 'prefix', 'path'}
    keeps = keys.intersection(d.keys())
    domain = ''
    elba = d.get('load_balancer_arn', '')

    key2 = key if 'self' not in key else ''
    raw = [d.get('host'), key2, d.pop('key', ''), d.get('upstrm'), d.pop('host_full', ''),
           d.pop('hostname', ''), d.get('serviceName'), d.get('url')]
    raw2 = [r for r in raw if r and isinstance(r, str) and is_ip_url(r)]
    raw1 = [r for r in raw if r and isinstance(r, str) and not is_ip_url(r)]
    raw = [url_to_shp(r, prt=d.get('port', '')) for r in raw1]

    if any([1 for r in raw if check_s3_name(r.get('hostname', '')) == AWS_S3_NAME]):
        host = AWS_S3_SHORT_NAME
        hfull = AWS_S3_NAME
        d.update({"host": host})
        d.update({"host_full": hfull})
        d.update({"domain": "amazonaws.com"})
    elif elba:
        host = d.get('serviceName') or first_valid([r.get('hostname', '') for r in raw])
        hfull = d.get('upstrm') or first_valid([r.get('hostname', '') for r in raw])
        d.update({'public_dns_name': first_valid(key2, *[r.get('hostname', '') for r in raw])})
        port = first_valid([str(r.get('port', '')) for r in raw])
        d.pop('scheme', '')
        d.pop('domain', '')

        raw = [d.get('upstrm'), d.pop('host_full', '')]
        raw1 = [r for r in raw if r and isinstance(r, str) and not is_ip_url(r)]
        raw = [url_to_shp(r, prt=d.get('port', '')) for r in raw1]
        scheme = first_valid([r.get('scheme', '') for r in raw])
        domain = first_valid(*[r.get('domain', '').strip('. -') for r in raw],svc_domain.strip('. -'))
        hfull = url_to_shp(hfull).get('hostname', hfull)
        d.update({"host": host.strip('. -')})
        d.update({"host_full": hfull.strip('. -')})
        d.update({"port": port})
        d.update({"scheme": scheme})
        d.update({'domain': domain})

    else:
        host = first_valid([r.get('hostname', '') for r in raw])
        port = first_valid([str(r.get('port', '')) for r in raw])
        scheme = first_valid(d.get("scheme", ''), *[r.get('scheme', '') for r in raw])
        domain = first_valid(d.get("domain", '').strip('. -'), *[r.get('domain', '').strip('. -') for r in raw],
                             svc_domain.strip('. -'))

        d.update({"port": port} if port else {})
        d.update({"scheme": scheme} if scheme else {})
        d.update({"domain": domain} if domain else {})
        prefix = d.get('prefix', '') or ''

        if host:
            fqdn = getfqdn(host)
            if len(fqdn) > len(host) and host in fqdn:
                dpp = fqdn.split(host, 1)
                # Check if there is an instance number
                if dpp[-1].startswith('-') and '.' in dpp[-1]:
                    dsplt = dpp[-1].strip('-').split('.', 1)
                    # Add the instance number if it exists
                    d['instance'] = dsplt[0] if dsplt[0].isdecimal() else d.get('instance') or ''
                    dpp[-1] = dsplt[1] if dsplt[0].isdecimal() else dpp[-1].strip('-')

                elif domain and dpp[-1].strip('. -') != domain:
                    print(f"[DEBUG] getfqdn returned domain {dpp[-1].strip('. -')} but domain {domain} was specified")

                domain = dpp[-1].strip('. -')
                d.update({"domain": domain} if domain else {})

                if len(dpp) > 1 and prefix and dpp[0].strip('. -') != prefix.strip('. -'):
                    print(f"[DEBUG] getfqdn returned prefix {dpp[-1].strip('. -')} but prefix {prefix} was specified")
                elif len(dpp) > 1:
                    prefix = dpp[0].strip('. -')
                    d.update({"prefix": prefix} if prefix else {})
        else:
            host = first_valid([url_to_shp(r).get('hostname', '') for r in raw2])

        port = d.get('port', '') or ''
        domain = d.get('domain', '') or ''
        prefix = d.get('prefix', '') or ''
        instance = d.get('instance', '') or ''

        host = host.split(':', 1)[0] if ':' in host else host
        host = host.replace(domain, '').strip('. -') if domain and domain in host else host
        host = host.replace(prefix, '').strip('. -') if prefix and prefix in host else host
        host = host.replace(instance, '').strip('. -') if instance and instance in host else host

        hfull = '-'.join([prefix, host, instance]).strip('. -')
        hfull = '.'.join([hfull, domain]).strip('.')
        if port and port != '443' and port != '80':
            hfull = ':'.join([hfull, port]).strip(':')

        if "amazonaws.com" in host or "amazonaws.com" in hfull:
            d.update({"domain": "amazonaws.com"})

        if "amazonaws.com" in host:
            d.update({"host": host.replace('.amazonaws.com', '').strip('. -')})

        if isinstance(hfull, str) and hfull:
            d.update({"host_full": hfull.strip('. -')})

        if isinstance(host, str) and host:
            if (host == os.getenv('CSI_ROLE_EXTERNAL_ID', '') or
                    host == os.getenv('CSI_TENANT_ID', '')  or
                    host == os.getenv('CSI_DEPLOYMENT_ID', '') or
                    host.count("newcopet") or hfull.count("newcopet")):
                print(f"[DEBUG] host {host} is a CSI ID.  Setting host to newco-nextcloud.caber.svc")
                d.update({"host": "newco-nextcloud.caber.svc"})  #FIXME: HACK!
                d.update({"hostname": None})
            else:
                d.update({"host": host.strip('. -')})

    return d


def url_to_shp(url: str, prt='', host='') -> dict:
    """
    Convert a url to a dict with scheme, hostname, and port.  Used mostly for validating configuration params.
    Discards any path or query.  After a reverse DNS lookup the url can be something like
    'http://ip-10-0-0-220.us-west-1.compute.internal:9200'. If so, extract the Ipv4 address, domain and return.

    This function purposely does not set keys 'host' or 'host_full' to avoid the calling function from
    potentially overwriting existing values for these keys.  Instead, it writes 'hostname' and leaves it to the
    calling function to replace host or host_full if needed.

    :param url: string representation of a url
    :return: dict with ['scheme', 'hostname', 'port', 'accessKey', 'secretKey', 'domain', 'region', 'ipv4', 'ipv6']
             keys as appropriate for the given input.
    """
    ret = {}
    domain = ''

    if isinstance(url, (str, bytes, bytearray)) and url:
        if '://' not in url:
            spl_url = urlsplit('foo://' + url)
        else:
            spl_url = urlsplit(url)

        pattern = r'^(?:[a-z]{0,10}-?)(\d{1,3}[-|\.]\d{1,3}[-|\.]\d{1,3}[-|\.]\d{1,3})'
        match = re.search(pattern, spl_url.hostname)

        if match:
            ip_addr = match.group(1).replace('-', '.')
            domain = spl_url.hostname.replace(match.group(0), '').strip('. -')
            ret = check_ip_address(ip_addr, no_zero=True, value_only=False)
            ret.update({"hostname": match.group(0)})
        else:
            ret = check_ip_address(spl_url.hostname, no_zero=True, value_only=False)
            if not ret and spl_url.hostname:
                ret = {"hostname": spl_url.hostname.strip('. -')}

        for region in get_aws_regions():
            if domain and region in domain:
                ret.update({"region": region})
                domain = domain.replace(region, '').strip('. -')
                break
            elif not domain and region in spl_url.hostname:
                ret.update({"region": region})
                break

        if (isinstance(prt, str) and prt.isdecimal() or isinstance(prt, int)) and 0 < int(prt) < 65536:
            ret.update({"port": int(prt)})

        elif spl_url.port and str(spl_url.port).isdecimal() and 0 < int(spl_url.port) < 65536:
            ret.update({"port": int(spl_url.port)})

        ret.update({"scheme": spl_url.scheme} if spl_url.scheme != 'foo' else {})
        ret.update({'accessKey': spl_url.username})
        ret.update({'secretKey': spl_url.password})
        ret.update({"domain": domain})

    out =  {k: v for k, v in ret.items() if isinstance(v, bool) or v}

    return out


def check_ip_address(is_ip, no_zero=False, value_only=False):
    """
    Checks for a valid IPv4 or IPv6 address and returns it.
    :param is_ip: The value to test
    :param no_zero: Don't return '0.0.0.0' as a valid IPv4 address
    :param value_only: return just the IP address if True, otherwise return {'ipv4': IP}
    :return:
    """

    try:
        ip = ip_address(is_ip)
    except (ValueError, AddressValueError):
        return '' if value_only else {}
    else:
        ipc = str(ip.compressed).strip()
        if isinstance(ip, IPv4Address):
            if no_zero and ipc == "0.0.0.0":
                return '' if value_only else {}
            return  ipc if value_only else {"ipv4": ipc}
        else:
            return ipc if value_only else {"ipv6": ipc}


def combine_shps(shpa: dict, shpb: dict) -> dict:
    """
    Given two dicts with scheme, hostname, port, etc., that may each be missing some values, create one
    dict with a complete set of values giving precedence to shpa -- that is, if shpa and shpb both have a 
    value for, say, 'host', then shpa[host] will be in the output.  Ensure that the username and password
    are passed as a unit.
    
    :param shpa: dict with {'scheme': '', 'host': '', 'port': '', 'accessKey': '', 'secretKey': ''}
    :param shpb: dict with {'scheme': '', 'host': '', 'port': '', 'accessKey': '', 'secretKey': ''}
    :return: dict with {'scheme': '', 'host': '', 'port': '', 'accessKey': '', 'secretKey': ''}
    """
    
    out = {}

    keys = set(shpa.keys()).union(shpb.keys()).difference(["accessKey", "secretKey", "ipv4", "ipv6"])

    if shpa.get("accessKey", "") and shpa.get("secretKey", ""):
        out.update({'accessKey': shpa["accessKey"], 'secretKey': shpa["secretKey"]})
    elif shpb.get("accessKey", "") and shpb.get("secretKey", ""):
        out.update({'accessKey': shpb["accessKey"], 'secretKey': shpb["secretKey"]})
    elif shpa.get("accessKey", "") and not shpb.get("accessKey", "") or \
            shpa.get("secretKey", "") and not shpb.get("secretKey", ""):
        out.update({'accessKey': shpa.get("accessKey", ""), 'secretKey': shpa.get("secretKey", "")})
    else:
        out.update({'accessKey': shpb.get("accessKey", ""), 'secretKey': shpb.get("secretKey", "")})

    ipv4s = shpa.get("ipv4", []) or []
    ipv4s.extend(shpb.get("ipv4", []) or [])
    ipv4s.append([shpa.get("host") or "", shpb.get("host") or ""])
    ipv4s = [ ip for ip in ipv4s if check_ip_address(ip, no_zero=True, value_only=True)]
    ipv4s = [i for i in ipv4s if i]
    ipv6s = shpa.get("ipv6", []) or []
    ipv6s.extend(shpb.get("ipv6", []) or [])
    ipv6s = [ ip for ip in ipv6s if check_ip_address(ip, no_zero=True, value_only=True)]
    ipv6s = [i for i in ipv6s if i]
    out.update({"ipv4": ipv4s}) if ipv4s else None
    out.update({"ipv6": ipv6s}) if ipv6s else None

    for k in keys:
        result = b_if_not_a(shpa.get(k), shpb.get(k))
        out.update({k: result})
    #
    # out.update({'region': b_if_not_a(shpa.get("region", ""), shpb.get("region", ""))})
    # out.update({'scheme': b_if_not_a(shpa.get("scheme", ""), shpb.get("scheme", ""))})
    # out.update({'host': b_if_not_a(shpa.get("host", ""), shpb.get("host", ""))})
    # out.update({'host_full': b_if_not_a(shpa.get('host_full', ""), shpb.get('host_full', ""))})
    # out.update({'port': b_if_not_a(shpa.get("port", ""), shpb.get("port", ""))})
    # out.update({'open_port': b_if_not_a(shpa.get("open_port", ""), shpb.get("open_port", ""))})
    # out.update({'use_ssl': b_if_not_a(shpa.get("use_ssl"), shpb.get("use_ssl"))})
    # out.update({'is_up': b_if_not_a(shpa.get("is_up"), shpb.get("is_up"))})
    # out.update({'upstrm': b_if_not_a(shpa.get("is_up"), shpb.get("is_up"))})
    # out.update({'initialized': b_if_not_a(shpa.get("initialized"), shpb.get("initialized"))})
    # out.update({'enabled': shpa.get("enabled", False) or shpb.get("enabled", False)})

    return {k: v for k, v in out.items() if v is not None and v != ''}


def shp_to_port(shp: dict):
    """
    Look for a service port in the host configuration (shp).  If not implied by the scheme (that is, 80 or 443),
    the service port should be an integer value under the key 'port'.  However, it may also be specified as the
    first entry in a list of ports under the key 'ports', or, if the key 'ports' contains a dict, then under the
    key 'service'.  If all that fails, see if host_full has a port, or take the first port in a dict that is not
    a debug port, then use it.

    :param shp:  Dictionary containing host configuration parameters.
    :return:  Dictionary containing host configuration parameters with the port key updated.
    """

    def _gsp(x):
        if x:
            a = str(x) if isinstance(x, (str, int)) and str(x).isdecimal() else ''
            b = str(x[0]) if isinstance(x, list) and len(x) > 0 and str(x[0]).isdecimal() else ''
            c = ''
            if isinstance(x, dict) and len(x.keys()):
                vees = [str(v) for k, v in x.items() if k.lower() not in ['debug', 'service'] and str(v).isdecimal()]
                if str(x.get("service", "")).isdecimal():
                    c = str(x["service"])
                elif len(vees):
                    c = vees[0]
            return first_valid(a, b, c)
        return

    p1 = _gsp(shp.get("port"))
    p2 = _gsp(shp.get("ports"))
    p3 = _gsp(shp.get("host_full", "").rsplit(':', 1)[-1])

    service_port = first_valid(p1, p2, p3)
    if service_port:
        shp.update({"port": service_port})
    return shp


def shp_to_url(shp: dict, include_auth=True, rtn='all') -> str:
    """
    Convert a dict with scheme, hostname, and port to a url.  Used mostly for validating configuration params.
    Discards any path or query.  For consistency, always give precedence to the explicit value, i.e., port = 9975, rather than
    the implicit value i.e., hostname:3476.

    :param include_auth: If True and if username or password exist, add them to the url (default=True)
    :param shp: dict with {'scheme': '', 'host': '', 'port': '', 'accessKey': '', 'secretKey': ''}
    :param rtn: If rtn == 'all' the return value will be a list of all valid urls, else it will return only the
                first valid url.
    :return:  string representation of a url
    """
    
    def _construct_url(_hostname, _shp, _include_auth, _scheme):

        hs = _hostname.rsplit(':', 1)
        port = ''
        if len(hs) == 2:
            port = hs[-1]
            host_no_port = hs[0]
        else:
            host_no_port = _hostname

        # Don't add ports 80 or 443 to urls that imply them.  Also keeps us from putting port 80 on an https url.
        proto = b_if_not_a(_shp.get('scheme', ''), _scheme)
        port = '' if str(port) in ["80", "443"] and proto in ["http", "https"] else port
        sport = '' if str(_shp.get('port')) in ["80", "443"] and proto in ["http", "https"] else _shp.get('port', '')
        port = b_if_not_a(sport, port)

        if _include_auth and (_shp.get("accessKey", "") or _shp.get("secretKey", "")):
            url = f"{proto}://{_shp.get('accessKey', '')}:{_shp.get('secretKey', '')}@{host_no_port}"
        else:
            url = f"{proto}://{host_no_port}"

        if port:
            url = f'{url}:{port}'

        if is_valid_endpoint_url(url):
            return url
        return

    # ===================================================================================================

    scheme = "http" if shp.get("use_ssl", False) else 'http'
    scheme = shp.get("scheme", scheme)

    if not shp.get('domain', '') and shp.get('host_full', '').count('.'):
        dtry = shp['host_full'].split('.', 1)[-1]
    else:
        dtry = shp.get('domain', '')

    invalid = "{_}"
    hostname = [shp.get("host_full", invalid),
                shp.get("host_full", "").replace(dtry, '').replace(".:", ":"),
                f"{shp.get('host', invalid)}.{shp.get(dtry, '')}".strip('.: -'),
                shp.get("host", invalid),
                shp.get("ipv4", invalid),
                shp.get("ipv6", invalid)]

    ids_to_drop = [os.getenv("CSI_ROLE_EXTERNAL_ID"), os.getenv("CSI_TENANT_ID"), os.getenv("CSI_DEPLOYMENT_ID")]
    hostname = [h for h in hostname if h not in ids_to_drop]

    urls = [_construct_url(h, shp, include_auth, scheme) for h in hostname if h and isinstance(h, str)]

    if rtn != 'all':
        urls = first_valid(urls)
    else:
        urls = [u.strip('. -') for u in urls if u]
        urls = list(set(urls))

    if not urls:
        print(f"[WARNING] shp_to_url: No valid hostname found to construct url")
        return "" if rtn != 'all' else []

    return urls


def fill_shp_from_url(url: str, shp: dict, reverse=False) -> dict:
    """
    Explode url in standard host dictionary and fill in the standard
    :param url:
    :param shp:
    :param reverse:
    :return:
    """
    port = shp.get('port', '')
    if reverse:
        return combine_shps(shp, url_to_shp(url, port))
    else:
        return combine_shps(url_to_shp(url, port), shp)


def fnfilter_list(input_list: list, pattern_list: list):
    ret = chain.from_iterable(fnfilter(input_list, pat) for pat in pattern_list)
    return list(ret)


def split_string_list(ss: str, delim=','):
    sl = [ss]
    if ss.startswith('[') and ss.endswith(']'):
        try:
            sl = json.loads(ss)
        except json.JSONDecodeError as err:
            print(f"[WARNING] Ignoring Bad JSON list: {err}")

    elif ' ' in ss or delim in ss:
        ss = ss.replace(' ', delim)
        sl = [s.strip(delim + '[]{}()') for s in ss.split(delim) if s]

    return sl

