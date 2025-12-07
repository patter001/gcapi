import time
import hashlib
import base64
from requests import Session, Request
from pprint import pformat
from logging import getLogger

from qcapi._object import ObjectEndpoint
from ._backtests import Backtests
from ._live import LiveEndpoint
from ._compile import CompileEndpoint
from .errors import QCException
from typing import Type, TypeVar, TYPE_CHECKING, overload

if TYPE_CHECKING:
    from requests import Response

T = TypeVar("T")

_LOG = getLogger("qcapi")

class QCClient:
    url: str = ""
    token: str = ""
    backtests: "Backtests"

    def __init__(self, url, user_id, token, *, timeout=30):
        self.url = url
        self.user = user_id
        self.token = token
        self._timeout = timeout
        self.backtests = Backtests(self, "/backtests")
        self.live = LiveEndpoint(self, "/live")
        self.object = ObjectEndpoint(self, "/object")
        self.compile = CompileEndpoint(self, "/compile")

    @property
    def _session(self) -> Session:
        # Get timestamp
        # not sure of the importance here but we could make this smarter by just redoing the
        # timestamp code every X seconds
        # currently the QC timeout appears to be two hours, and if you reuse
        # the header for more than 2 hours it will fail
        timestamp = str(int(time.time()))
        time_stamped_token = f"{self.token}" + ":" + timestamp
        hashed_token = hashlib.sha256(time_stamped_token.encode("utf-8")).hexdigest()
        authentication = "{}:{}".format(self.user, hashed_token)
        api_token = base64.b64encode(authentication.encode("utf-8")).decode("ascii")
        headers = {
            "Authorization": f"Basic {api_token}",
            "Timestamp": timestamp,
        }
        session = Session()
        session.headers.update(headers)
        return session

    @overload
    def request(
        self, method: str, url: str, *, json: dict | None = None, params: dict | None = None, response_type: Type[T]
    ) -> T: ...

    @overload
    def request(
        self, method: str, url: str, json: dict | None = None, params: dict | None = None, response_type: None = None
    ) -> "Response": ...

    def request(
        self,
        method: str,
        url: str,
        json: dict | None = None,
        params: dict | None = None,
        response_type: Type[T] | None = None,
    ) -> T | "Response":
        request = Request(method, f"{self.url}{url}", json=json, params=params)
        prepared_request = self._session.prepare_request(request)
        first_time = time.time()
        while True:
            response = self._session.send(prepared_request, timeout=self._timeout)
            response.raise_for_status()
            resp_data = response.json()
            # if loading, keep polling until we hit the timeout
            if response.json().get("status", None) == "loading" and time.time() - first_time < self._timeout*2:
                continue
            elif not resp_data.get("success", True):
                errors = resp_data.get("errors", None)
                if errors is not None and len(errors) > 0:
                    error_str = errors[0]
                else:
                    error_str = "Unknown error"
                msg = f"QC error for {url}\n\t{error_str}"
                _LOG.info(msg)
                _LOG.info("Response data: ")
                _LOG.info(resp_data)
                raise QCException(f"QC error for {url}\n\t{error_str}", errors=errors)
            else:
                break

        if response_type:
            try:
                return response_type(**response.json())
            except Exception:
                with open("errors.json", "w") as f:
                    f.write(pformat(response.json()))
                raise
        else:
            return response
