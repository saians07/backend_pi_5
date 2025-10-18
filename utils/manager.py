# pylint: disable=W0611
"""
    Inject all clients, object classes, and tables needed by the main application
"""
from fastapi import FastAPI
import httpx

async def lifespan(app: FastAPI):
    """
        Preparing objects and clients for each fastapi worker
    """
    httpx_client = httpx.AsyncClient(
        timeout=httpx.Timeout(60.0, connect=10.0),
        limits=httpx.Limits(
            max_connections=30,
            max_keepalive_connections=5
        ),
    )
    app.state.httpx_client = httpx_client

    yield
    await app.state.httpx_client.aclose()
