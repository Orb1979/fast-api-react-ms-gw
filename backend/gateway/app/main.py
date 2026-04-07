from urllib.parse import urlencode

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status

from .auth import require_jwt
from .config import settings

app = FastAPI(title="gateway-service")


@app.get("/public/gateway")
def public_gateway() -> str:
    return "Hit public gateway (no JWT required)"


@app.get("/gateway")
def private_gateway(claims: dict = Depends(require_jwt)) -> str:
    return f"Hit secure gateway, {claims.get('sub')}"


@app.api_route(
    "/api/{service_key}/{downstream_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def forward_request(
    service_key: str,
    downstream_path: str,
    request: Request,
    _claims: dict = Depends(require_jwt),
) -> Response:
    base_url = settings.services.get(service_key)
    if base_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown service: {service_key}",
        )

    query = urlencode(list(request.query_params.multi_items()), doseq=True)
    target_url = f"{base_url.rstrip('/')}/{downstream_path.lstrip('/')}"
    if query:
        target_url = f"{target_url}?{query}"

    body = await request.body()
    outbound_headers = {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in {"host", "content-length"}
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        upstream = await client.request(
            method=request.method,
            url=target_url,
            headers=outbound_headers,
            content=body if body else None,
        )

    hop_by_hop = {"transfer-encoding", "connection", "keep-alive"}
    response_headers = {
        k: v for k, v in upstream.headers.items() if k.lower() not in hop_by_hop
    }
    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers=response_headers,
        media_type=upstream.headers.get("content-type"),
    )
