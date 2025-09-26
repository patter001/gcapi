import time
import hashlib
import base64
from requests import Session, Request
from pprint import pformat

from qcapi._object import ObjectEndpoint
from ._backtests import Backtests
from ._live import LiveEndpoint
from .errors import QCException
from typing import Type, TypeVar, TYPE_CHECKING, overload

if TYPE_CHECKING:
    from requests import Response

T = TypeVar("T")


class QCClient:
    url: str = ""
    token: str = ""
    backtests: "Backtests"

    def __init__(self, url, user_id, token, *, timeout=60):
        self.url = url
        self.user = user_id
        self.token = token
        self._timeout = timeout

        # Get timestamp
        self._timestamp = str(int(time.time()))
        time_stamped_token = f"{token}" + ":" + self._timestamp
        hashed_token = hashlib.sha256(time_stamped_token.encode("utf-8")).hexdigest()
        authentication = "{}:{}".format(self.user, hashed_token)
        self._api_token = base64.b64encode(authentication.encode("utf-8")).decode("ascii")
        self._headers = {
            "Authorization": f"Basic {self._api_token}",
            "Timestamp": self._timestamp,
        }
        self._session = Session()
        self._session.headers.update(self._headers)
        self.backtests = Backtests(self, "/backtests")
        self.live = LiveEndpoint(self, "/live")
        self.object = ObjectEndpoint(self, "/object")

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
            response = self._session.send(prepared_request)
            response.raise_for_status()
            resp_data = response.json()
            # if loading, keep polling until we hit the timeout
            if response.json().get("status", None) == "loading" and time.time() - first_time < self._timeout:
                continue
            elif not resp_data.get("success", True):
                raise QCException(f"QC error for {url}", errors=resp_data.get("errors", None))
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
