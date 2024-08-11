import os
import sys

from fastapi import FastAPI, Request

# from starlette.middleware.cors import CORSMiddleware
# import asyncio

from pydantic import BaseModel
from typing import List
from pprintpp import pprint

from datetime import datetime
now = datetime.now()
date_time_format = now.strftime("%Y%m%d_%H%M%S")

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

# request from ChangeDetection.io
# class CdioRequest(BaseModel):
#     version: str
#     name: str
#     url: str
#     source: str
#     created_at: str = date_time_format
    
   
# trigger scraper when post request is received from cdio 
@app.post("/trigger")
async def post_cdio_json(request: Request):
    pprint(request)
    return await request.json()




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.getenv("PORT", 8000))


    # uvicorn.run(app, host="127.0.0.1", port=8000)
