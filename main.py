# pylint: disable=C0114
from fastapi import FastAPI, Request

app = FastAPI(title="Backend Raspberry Pi")

@app.get("/")
def root():
    return {'status': "error"}

@app.get("/health")
def health(): # pylint: disable=C0116
    return {'status': "ok", 'status_code': 200}
