import os
import sys
import uvicorn

from fastapi import FastAPI, Request

# from starlette.middleware.cors import CORSMiddleware
# import asyncio

from pydantic import BaseModel

app = FastAPI()

# allowed_origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
#     "https://localhost:44345/",
#     "https://localhost:44345",
# ]

# allowed_origins = ["*"]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["X-Requested-With", "Content-Type"],
#     allow_origins=allowed_origins,
# )


class CdioJson(BaseModel):
    version: str
    title: str
    message: str
    type: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/cdio")
async def post_cdio_json(request: Request):
    return await request.json()



if __name__ == "__main__":
    # uvicorn.run("tts_server:app", host="127.0.0.1", port=8000, log_level="info")

    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="127.0.0.1", port=port)
