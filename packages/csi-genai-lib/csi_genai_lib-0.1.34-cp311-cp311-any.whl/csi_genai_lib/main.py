# ##################################################################################################
#  Copyright (c) 2024.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  main.py                                                                              #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

import base64
import json

from datetime import timezone, datetime
import urllib3

from csiMVP.Common.streamtap import StreamTap
from csiMVP.Common.init import CFG, post_status_message, get_primary_ip, gethostname, beginning_of_time
from csiMVP.Toolbox.sqs_init import post2queue, get_queue
from csiMVP.Toolbox.json_encoder import extEncoder
from csiMVP.Toolbox.obo import request_obo, response_obo, original_call_terminated

urllib3.disable_warnings()   # Gets rid of annoying self-signed cert errors

VERSION = "csi-genai-lib-0.1.0"
noB64encode = ['text/html', 'text/css', 'text/plain', 'text/xml', 'application/x-www-form-urlencoded',
               'application/javascript', 'application/json', 'application/xhtml+xml']

CRLF = '\n'
request_session_hold = None
queue = None
normal_ops = 0


class MainHandler:
    """
    The MainHandler class is responsible for handling API requests and responses for the GenAI Chat Library.

    This class provides methods to create a new request, update the response, and post the event to an SQS queue
    for further processing. It captures request and response data, including headers, body, and metadata, and
    prepares an SQS message with the captured information.

    Attributes:
        SUPPORTED_METHODS (tuple): A tuple of supported HTTP methods.
        reqB64encode (bool): Flag indicating whether to base64 encode the request body.
        request (dict): Dictionary containing the request information.
        isStream (bool): Flag indicating if the request is a stream.
        dest_host (str): Destination host for the request.
        path (str): API path for the request.
        req_timeout (int): Request timeout in seconds.
        default_method (str): Default HTTP method for the request.
        allow_redirects (bool): Flag indicating whether to allow redirects.
        auth (dict): Dictionary containing user authentication information.
        _sqs_message (dict): Dictionary representing the SQS message to be sent.
        updata (str): Request body data.
        apirsp (object): API response object.
        apimap (dict): API mapping configuration.
        dest_url (str): Destination URL for the request.
        req_id (str): Unique request ID.
        req_tap (StreamTap): StreamTap object for capturing request data.
        rsp_tap (StreamTap): StreamTap object for capturing response data.
        session (str): User session identifier.
        req_phdrs (dict): Dictionary containing request headers.
        rsp_phdrs (dict): Dictionary containing response headers.
        query (str): Query string for the request.
        user_session (str): User session identifier.
        user_host (str): User hostname or IP address.
        port (int): Port number for the request.
        mime (str): MIME type for the request and response.
        ready_to_post (int): Flag indicating the readiness to post the event.

    Methods:
        __init__(**kwargs): Initializes a new instance of the MainHandler class.
        new_request(**kwargs): Creates a new request with the provided parameters.
        post_event(): Posts the captured event to an SQS queue.
        update_response(**kwargs): Updates the response with the provided parameters.
    """

    SUPPORTED_METHODS = ('GET', 'HEAD', 'POST', 'DELETE', 'PUT', 'PATCH', 'OPTIONS',
                         'PROPFIND', 'MKCOL', 'MOVE', 'LOCK', 'UNLOCK', 'PROPPATCH')
    reqB64encode = False
    request = {}
    isStream = False
    dest_host = gethostname()
    path = 'chat-post'
    req_timeout = 10
    default_method = "POST"
    allow_redirects = True
    auth = {"user.id": "noAuth", "user.type": "basic"}
    _sqs_message = {}
    updata = ''
    apirsp = None
    apimap = None
    dest_url = ''
    req_id = 'should be a uuid here'
    req_tap = None
    rsp_tap = None
    session = ''
    req_phdrs = {}
    rsp_phdrs = {}
    obo = {}
    query = None
    user_session = None
    user_host = "unknown.nosession"
    port = 80
    mime = 'application/json; charset=utf-8'
    ready_to_post = 0
    _request_time = beginning_of_time

    def __init__(self, **kwargs) -> None:
        self._sqs_message = {"R.ID": "", "event.time": beginning_of_time, "R.VERSION": VERSION,
                             'R.API': '', 'C.REQ': {}, 'C.RSP': {}}
        self.ready_to_post = 0
        try:
            post_status_message(stage="3.0", message="Entering normal operation", status="green")
        except Exception as e:
            pass

    @property
    def sqs_message(self) -> dict:
        if self.ready_to_post == 0:
            return {}
        return self._sqs_message    

    def convert_updata(self, charset='utf-8') -> None:
        if isinstance(self.updata, (dict, list)):
            self.updata = json.dumps(self.updata)
            self.updata = self.updata.encode(charset)
        elif isinstance(self.updata, str):
            self.updata = base64.b64decode(self.updata) if self.reqB64encode else self.updata.encode(charset)
        elif not isinstance(self.updata, bytes):
            self.updata = str(self.updata).encode(charset)

    def new_request(self, **kwargs) -> None:
        global normal_ops
        self.updata = kwargs.get('context') or ''
        self.reqB64encode = kwargs.get('base64') or False
        self.dest_host = kwargs.get('hostname') or get_primary_ip()
        self.req_timeout = kwargs.get("req_timeout") or 10
        self.default_method = kwargs.get("default_method") or "POST"
        self.auth = {"user.id": kwargs.get("user_id", "noAuth"), "user.type": kwargs.get("user_type", "basic")}
        self.user_host = kwargs.get('user_hostname_or_ip') or "unknown." + str(kwargs.get('user_session', 'nosession'))
        self.user_session = kwargs.get('user_session') or None
        self.path = kwargs.get('api_name') or 'chat-post'
        self.mime = kwargs.get('mime_type') or 'application/json; charset=utf-8'
        self.query = kwargs.get('query') or None
        self.req_id = CFG.new_id()
        self.req_tap = None
        self.rsp_tap = None
        self.req_phdrs = {}
        self.rsp_phdrs = {}
        self.port = 80
        self._request_time = datetime.now(timezone.utc)

        self.path = self.path.strip('/')
        if isinstance(self.dest_host, str) and self.dest_host.endswith('/'):  # Drop trailing '/'
            self.dest_host = self.dest_host[:-1]

        psswd = base64.b64encode(f'{self.auth.get("user.id", "noAuth")}:abc123'.encode('utf-8')).decode('utf-8')

        self._sqs_message = {
            "R.ID": self.req_id,
            "event.id": self.req_id,
            "event.time": self._request_time.isoformat(),
            "R.VERSION": VERSION,
            'R.API': f'{self.dest_host}/{self.path}',
            'api.host.name': self.dest_host,
            'api.path': self.path,
            "api.scheme": "https",
            "user.id": kwargs.get("user_id", "noAuth"),
            "user.type": kwargs.get("user_type", "basic"),
            "sourceIPAddress": self.user_host,
            'user.from.host.ip': self.user_host,
            # 'user.from.host.name': self.user_host,
            'C.REQ': {
                "method": self.default_method,
                "host": self.dest_host,
                "path": self.path,
                "base64": False,
                "body": "",
                "headers": {
                    "Host": self.dest_host,
                    "User-Agent": VERSION,
                    'Content-Type': self.mime,
                    'Content-Length': 0,
                    "Authorization": f"{self.auth.get('user.type', 'basic').capitalize()} {psswd}",
                },
            },
            'C.RSP': {
                "code": 200,
                "base64": False,
                "body": "",
                "headers": {},
            }
        }

        normal_ops += 1
        if CFG.post_log_now:
            post_status_message(stage="3.1", message=f"Processing API request {normal_ops}", status="green")

        if self.query is not None:
            self._sqs_message.update({'R.ARGS': f'{self.query}'})
            self._sqs_message['C.REQ'].update({'query': f'{self.query}'})

        if self.user_session is not None:
            self._sqs_message.update({'user.session': self.user_session})

        req_blen = self.request.get('headers', {}).get('Content-Length') or len(self.request.get('body', ''))
        req_type = self.mime
        if isinstance(req_type, str):
            req_type = req_type.split('; ')
        if len(req_type) == 1:
            req_type.append('charset=utf-8')
        charset = req_type[1].split('=')[-1] or 'utf-8'

        self.reqB64encode = False if req_type[0] in noB64encode else True
        self.convert_updata(charset)

        req_blen = len(self.updata)
        xuid = f'REQ-{self.req_id[-16:]}'
        print(f"[{self.req_id[-12:]}] RQST Buffered data: Type={req_type}  Length={req_blen}")
        self.req_tap = StreamTap(self.updata, chunk_size=req_blen, uid=xuid)
        self.req_tap.read()

        # Check if configured to post to SQS for the current status code
        # codeRe is regex pattern for matching status codes
        if self.req_tap is not None:
            if not self.req_tap.closed:
                self.req_tap.close()
            if self.req_tap.result is not None:
                self._sqs_message['C.REQ'].update({"sha256": self.req_tap.sha256})
                if isinstance(self.req_tap.result, str):
                    self._sqs_message['C.REQ'].update({"body": self.req_tap.result})
                elif self.reqB64encode:
                    self._sqs_message['C.REQ'].update({"body": base64.b64encode(self.req_tap.result).decode('utf-8')})
                    self._sqs_message['C.REQ'].update({"base64": True})
                else:
                    self._sqs_message['C.REQ'].update({"body": self.req_tap.result.decode('utf-8')})
                self._sqs_message['C.REQ']['headers'] |= {'Content-Length': req_blen}
                pmsg = self._sqs_message["C.REQ"]["body"][0:80].replace(CRLF, '')
                print(f'[{self.req_id[-12:]}] RQST Data tap result => {pmsg} self.req_tap.result={self.req_tap.result}')

                obo = request_obo(self.req_tap.result, req_type[0], kwargs.get("user_id", "noAuth"), self.req_id)
                if isinstance(obo, dict):
                    self.obo = obo
                    self._sqs_message |= obo
                else:
                    self.obo = {"obo_user": kwargs.get("user_id", "noAuth"), "obo_api": self.req_id}
                    self._sqs_message |= self.obo

        self.ready_to_post = 1

    def post_event(self) -> None:
        if self.ready_to_post != 2:
            raise RuntimeError("Not ready to post:  You must call new_request(), update_response() first")

        self.ready_to_post = 0

        message = json.dumps(self._sqs_message, cls=extEncoder)
        if len(message) < 262143:
            sqs_queue = get_queue("APIshdwQueue")
            # Send message to SQS queue for consumption by Process_API
            sqs_resp = post2queue(sqs_queue, message)

            if sqs_resp is not None:
                print(f"[{self.req_id[-12:]}] DONE: Tap posted to "
                      f"{sqs_queue.split('/')[-1]} "
                      f"({sqs_resp['MessageId']})")
            else:
                print(f"[{self.req_id[-12:]}] DONE: Post to SQS failed")
        else:
            print(
                f"[{self.req_id[-12:]}] DONE: No post to SQS: Message too big - {len(message)} > {CFG.me('maxSqsLen')}")

    def update_response(self, **kwargs) -> None:
        if self.ready_to_post != 1:
            raise RuntimeError("Not ready for response:  You must call new_request() first")

        delta_t = datetime.now(timezone.utc) - self._request_time
        latency = delta_t.total_seconds() * 1000
        self._sqs_message.update({"event.latency": latency})
        self._sqs_message.update({"latency_ms": latency})

        self.updata = kwargs.get('response') or None
        rsp_type = kwargs.get('mime_type') or 'application/json; charset=utf-8'

        data = True if self.updata is not None else False
        alen = len(self.updata) if data else 0
        rsp_params = {
            "code": 200,
            "base64": False,
            "sha256": "",
            "body": "",
            "headers": {
                'Content-Type': self.mime,
                'Content-Length': alen
            },
        }

        if isinstance(rsp_type, str):
            rsp_type = rsp_type.split('; ')
        if len(rsp_type) == 1:
            rsp_type.append('charset=utf-8')
        charset = rsp_type[1].split('=')[-1] or 'utf-8'
        rspB64encode = False if rsp_type[0] in noB64encode else True
        self.convert_updata(charset)

        xuid = f'RSP-{self.req_id[-16:]}'
        if int(alen) <= 0:
            print(f"[{self.req_id[-12:]}] RESP NO body")
        else:
            print(f"[{self.req_id[-12:]}] RESP Body: Type={rsp_type}  Length={alen}")
            self.rsp_tap = StreamTap(self.updata, chunk_size=alen, uid=xuid)
            self.rsp_tap.read()

            if not self.rsp_tap.closed:
                self.rsp_tap.close()
            if self.rsp_tap.result is not None:
                rsp_params.update({"sha256": self.rsp_tap.sha256})
                if isinstance(self.rsp_tap.result, str):
                    rsp_params.update({"body": self.rsp_tap.result})
                elif rspB64encode:
                    rsp_params.update({"body": base64.b64encode(self.rsp_tap.result).decode(charset)})
                    rsp_params.update({"base64": True})
                else:
                    rsp_params.update({"body": self.rsp_tap.result.decode(charset)})
                self._sqs_message['C.RSP']['headers'] |= {'Content-Length': alen}
                pmsg = self._sqs_message["C.RSP"]["body"][0:80].replace(CRLF, '')
                print(f'[{self.req_id[-12:]}] RESP Data tap result => {pmsg}')

                if self.req_id != self.obo.get('obo_api', ''):
                    response_obo(self.rsp_tap.result, self.rsp_phdrs.get("Content-Type", ""),
                                 self.obo.get('obo_user', ''), self.obo.get('obo_api', ''))

            if self.req_id == self.obo.get('obo_api', ''):
                original_call_terminated(self.req_id)

        self._sqs_message.update({'C.RSP': rsp_params})
        self.ready_to_post = 2
        self.post_event()
