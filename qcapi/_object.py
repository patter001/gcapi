from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel


if TYPE_CHECKING:
    from .._client import QCClient


class ObjectEndpoint:
    def __init__(self, client: "QCClient", url):
        self._client = client
        self._url = url

    def get(
        self,
        organization_id,
        keys: Optional[list[str]] = None,
        job_id: Optional[str] = None,
    ):
        if keys:
            data = dict(organizationId=organization_id, keys=keys)
        elif job_id:
            data = dict(organizationId=organization_id, jobId=job_id)
        else:
            raise TypeError("Must specify job or keys")
        return self._client.request(
            "GET",
            f"{self._url}/get",
            json=data,
            response_type=GetObjectStoreResponse,
        )


class GetObjectStoreResponse(BaseModel):
    jobId: Optional[str]
    url: Optional[str]
    success: bool
    errors: list
