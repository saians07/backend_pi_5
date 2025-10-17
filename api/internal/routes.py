from fastapi import APIRouter, status, HTTPException

internal_router = APIRouter(prefix="")

@internal_router.get("/", status_code=status.HTTP_403_FORBIDDEN)
def root():
    """Visit root path"""
    raise HTTPException(status_code=403, detail="Forbidden")

@internal_router.get("/health")
def health():
    """Check health for the page"""
    return {'status': "ok", 'status_code': status.HTTP_200_OK}