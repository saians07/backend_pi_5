# pylint: disable=C0114
from fastapi import FastAPI

app = FastAPI(title="Backend Raspberry Pi")

@app.get("/")
def root():
    """Visit root path"""
    return {'status': "error"}

@app.get("/health")
def health(): # pylint: disable=C0116
    """Check health for the page"""
    return {'status': "ok", 'status_code': 200}
