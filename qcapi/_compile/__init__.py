from pydantic import BaseModel
from typing import TYPE_CHECKING, Literal, Optional

if TYPE_CHECKING:
    from .._client import QCClient

class CompileEndpoint:
    def __init__(self, client: "QCClient", url):
        self._client = client
        self._url = url

    def create(self, project_id: str | int):
        return self._client.request(
            "POST",
            f"{self._url}/create",
            json=dict(projectId=project_id),
            response_type=CompileResponse,
        )

    def read(self, project_id: str | int, compile_id: str) -> "CompileReadResponse":
        return self._client.request(
            "GET",
            f"{self._url}/read",
            json=dict(projectId=project_id, compileId=compile_id),
            response_type=CompileReadResponse,
        )

class CompileReadResponse(BaseModel):
    compileId: str
    state: Literal['InQueue', 'BuildSuccess', 'BuildError']
    success: bool
    errors: Optional[list[str]] = None
    logs: Optional[list[str]] = None
    
class CompileResponse(CompileReadResponse):
    projectId: int
    parameters: list # this was empty in my test
    signature: str
    signatureOrder: list[str]

