# pylint: disable=C0114
from fastapi import FastAPI, HTTPException, status
from api import telegram_router

app = FastAPI(title="Backend Raspberry Pi")

@app.get("/", status_code=status.HTTP_403_FORBIDDEN)
def root():
    """Visit root path"""
    raise HTTPException(status_code=403, detail="Forbidden")

@app.get("/health")
def health():
    """Check health for the page"""
    return {'status': "ok", 'status_code': status.HTTP_200_OK}

# include telegram route
app.include_router(telegram_router)
