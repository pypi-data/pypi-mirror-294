# ##################################################################################################
#  Copyright (c) 2024.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  If used, attribution of open-source code is included where required by original author          #
#                                                                                                  #
#  Filename:  obo.py                                                                               #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

from pytz import utc
from csiMVP.Common.sequence import extract_and_index
from csiMVP.Toolbox.consolidate import CFG, ESP, pd, nan, match_in_index, datetime

esp = None
index = "csi_on_behalf_of"
dfcols = ["nmer", "obo_user", "obo_api", "junk", "event.time_request", "event.time_response"]


# # For a complete implementation we need to do the same here in API Tap that we did in S3 Scanner
# # paying attention to mime types, decoding documents, decompressing payloads, etc.
#   def _do_index_extract(ob):
#       ofn = FileNames(ob['object.id'])
#       ofn, result = extract_and_index(CFG, ofn, content_type=ob['object.mime_type'],
#                                       expected_hash=ob.get('object.sha256'))

# For the quick and dirty implementation we will assume that all payloads are uncompressed plain text
# This is typical for the RagChat demo.


def _obo(body, mime_type):
    global esp
    if esp is None:
        esp = ESP(CFG)

    _, result = extract_and_index(CFG, body, content_type=mime_type, return_hashlist=True)
    nmers = result.get('data.nmers.list', [])
    matches = match_in_index(nmers, index=index, return_cols="*", op="is", col_filters="nmer")
    return matches, nmers


def request_obo(body, mime_type, api_user, api_id):
    retval = {}
    now = datetime.now(tz=utc)
    matches, nmers = _obo(body, mime_type)

    if isinstance(matches, (pd.DataFrame, pd.Series)) and not matches.empty:
        not_junk = ~matches["junk"]
        not_expired = matches["event.time_response"].isna()
        obo_nmers = matches.loc[not_junk & not_expired, "nmer"]
        new_nmers = set(nmers).difference(matches["nmer"].to_list())

        if new_nmers:
            reqdf = pd.DataFrame(columns=dfcols, index=new_nmers)

            if obo_nmers.shape[0] == 0:
                reqdf["obo_user"] = api_user
                reqdf["obo_api"] = api_id
                reqdf["event.time_request"] = now
                reqdf["junk"] = False
                reqdf["nmer"] = reqdf.index
                retval |= {"obo_user": api_user, "obo_api": api_id}
                r = esp.post_df_to_es(index, reqdf)
            else:
                locm = matches["nmers"].isin(obo_nmers)
                obo = matches.loc[locm].groupby("obo_user")
                obo_count = obo.count().max().max()
                obo_api = obo["obo_api"].max()
                obo_user = obo["obo_user"].max()
                reqdf["obo_user"] = obo_user
                reqdf["obo_api"] = obo_api
                reqdf["event.time_request"] = now
                reqdf["junk"] = False
                reqdf["nmer"] = reqdf.index
                retval |= {"obo_user": obo_user, "obo_api": obo_api}
                # r = esp.post_df_to_es(index, reqdf)
    else:
        reqdf = pd.DataFrame(columns=dfcols, index=nmers)
        reqdf["obo_user"] = api_user
        reqdf["obo_api"] = api_id
        reqdf["event.time_request"] = now
        reqdf["junk"] = False
        reqdf["nmer"] = reqdf.index
        retval |= {"obo_user": api_user, "obo_api": api_id}
        r = esp.post_df_to_es(index, reqdf)

    return retval


def response_obo(body, mime_type, api_user, api_id):
    retval = {}
    now = datetime.now(tz=utc)
    matches, nmers = _obo(body, mime_type)

    new_nmers = nmers

    # Assume this is called only when the response is to a request made on behalf of another user
    if isinstance(matches, (pd.DataFrame, pd.Series)) and not matches.empty:
        not_junk = ~matches["junk"]
        not_expired = matches["event.time_response"].isna()
        matched_obo = matches.loc[not_junk & not_expired]
        new_nmers = set(nmers).difference(matches["nmer"].to_list())

        # We know this API call was made on belhalf of user api_user, so if the nmers retreived from the index
        # are not marked as junk and have not expired, but came from a different user, then we need to mark them
        # as junk defined as an nmer belonging to more than one user.
        different_user = matched_obo.loc[matched_obo["obo_user"].ne(api_user)]

        if different_user.shape[0] > 0:
            new_nmers = new_nmers.difference(different_user["nmer"].to_list())
            different_user["junk"] = True
            r = esp.post_df_to_es(index, different_user)

    if new_nmers:
        reqdf = pd.DataFrame(columns=dfcols, index=new_nmers)
        reqdf["obo_user"] = api_user
        reqdf["obo_api"] = api_id
        reqdf["event.time_response"] = now
        reqdf["junk"] = False
        reqdf["nmer"] = reqdf.index
        retval |= {"obo_user": api_user, "obo_api": api_id}
        r = esp.post_df_to_es(index, reqdf)

    return retval


def original_call_terminated(api_id):
    """
    Here when the original API call, not made on behalf of another user, is terminated.  We need to delete all nmers
    associated with this API call that are not marked as junk so that they won't be used again.

    :param api_id:
    :return: number of nmers deleted
    """
    retval = 0
    to_delete = match_in_index(api_id, index=index, return_cols="*", op="is", col_filters="obo_api")

    if isinstance(to_delete, (pd.DataFrame, pd.Series)) and not to_delete.empty:
        not_junk = ~to_delete["junk"]
        to_delete = to_delete.loc[not_junk]
        retval = to_delete.shape[0]
        if to_delete.shape[0] > 0:
            r = esp.delete_df_items_from_es(index, to_delete)
            if r != retval:
                print(f"[WARNING]: original_call_terminated Expected {retval} items to be deleted from index but saw {r} items deleted instead")
            retval = r

    return retval

