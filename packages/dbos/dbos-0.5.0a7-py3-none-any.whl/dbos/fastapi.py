import uuid
from typing import Any, Callable

from fastapi import FastAPI
from fastapi import Request as FastAPIRequest

from .context import (
    EnterDBOSHandler,
    OperationType,
    SetWorkflowID,
    TracedAttributes,
    assert_current_dbos_context,
)

request_id_header = "x-request-id"


def get_or_generate_request_id(request: FastAPIRequest) -> str:
    request_id = request.headers.get(request_id_header, None)
    if request_id is not None:
        return request_id
    else:
        return str(uuid.uuid4())


class Request:
    """
    Serializable subset of the FastAPI Request object.

    Attributes:
        base_url(URL): Base of URL requested, as in application code
        client(Address): HTTP Client
        cookies(Dict[str, str]): HTTP Cookies
        headers(Headers): HTTP headers
        method(str): HTTP verb
        path_params(Dict[str,Any]): Parameters extracted from URL path sections
        query_params(QueryParams): URL query string parameters
        url(URL): Full URL accessed

    """

    def __init__(self, req: FastAPIRequest):
        self.headers = req.headers
        self.path_params = req.path_params
        self.query_params = req.query_params
        self.url = req.url
        self.base_url = req.base_url
        self.client = req.client
        self.cookies = req.cookies
        self.method = req.method


def setup_fastapi_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def dbos_fastapi_middleware(
        request: FastAPIRequest, call_next: Callable[..., Any]
    ) -> Any:
        attributes: TracedAttributes = {
            "name": str(request.url.path),
            "requestID": get_or_generate_request_id(request),
            "requestIP": request.client.host if request.client is not None else None,
            "requestURL": str(request.url),
            "requestMethod": request.method,
            "operationType": OperationType.HANDLER.value,
        }
        with EnterDBOSHandler(attributes):
            ctx = assert_current_dbos_context()
            ctx.request = Request(request)
            workflow_id = request.headers.get("dbos-idempotency-key", "")
            with SetWorkflowID(workflow_id):
                response = await call_next(request)
        return response
