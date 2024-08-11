from fastapi import FastAPI, Request
from pprintpp import pprint

from datetime import datetime

now = datetime.now()
date_time_format = now.strftime("%Y%m%d_%H%M%S")

app = FastAPI()


@app.post("/trigger")
async def post_cdio_json(request: Request):
    """
    trigger scraper when post request is received from cdio
    """
    pprint(request)
    return await request.json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=9009, log_level="info")
