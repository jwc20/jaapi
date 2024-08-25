
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import os
from datetime import datetime
import time
from pprintpp import pprint
import json

# from li_scraper import LinkedInScraper
from li_scraper_db import LinkedInScraperDB
# import WAASU # TODO

from sqlalchemy import create_engine
import dotenv

from collections import namedtuple

dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

@app.get("/")
def index():
    return {
        "author": "cjw",
        "project": {
            "name": "Job Aggregate API",
            "url": "https://github.com/jwc20/jaapi",
        },
        "endpoints": {"trigger": "/trigger"},
    }



@app.post("/trigger")
async def post_cdio_json(request: Request):
    """
    trigger scraper when a POST request is received from cdio
    """
    try:
        req = await request.json()
        if "message" not in req:
            raise HTTPException(status_code=400, detail="Missing 'message' in the request body")

        message = req["message"]

        if isinstance(message, str):
            message = json.loads(message)
            pprint(message)

        # LinkedIn
        if "watch_url" in message and "linkedin" in message["watch_url"]:
            num_pages = 5
            global_start_time = time.time()
            now = datetime.now()
            date_time_format = now.strftime("%Y%m%d_%H%M%S")
            print(date_time_format)

            # print(f"Scraping from {message["watch_url"]}")

            # Call li_scraper_db.py
            scraped_jobs = LinkedInScraperDB.scrape_linkedin_jobs(message["watch_url"], num_pages)

            try:
                conn_string = DATABASE_URL

                db = create_engine(conn_string)
                conn = db.connect()
                print("connected to postgres")
                # df = pd.DataFrame(data)
                print(f"Total {scraped_jobs.count} received.")
                scraped_jobs.results.to_sql(
                    "scraped_li_job_listings", con=conn, if_exists="append", index=False
                )
                print("saved to postgres")
            except Exception as e:
                print(e)
            
            global_end_time = time.time()
            global_elapsed_time = global_end_time - global_start_time
            print(f"Total time taken: {global_elapsed_time:.4f} seconds")
            print("Ending LinkedIn scraper")

        response_data = {"status": "success", "data": message}
        return JSONResponse(content=jsonable_encoder(response_data))

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing key in the request body: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


if __name__ == "__main__":
    import uvicorn

    # TODO: use multiple gunicorn worker processes -> 16 workers since my cx33 server has 8 vCPU
    uvicorn.run("main:app", host="127.0.0.1", port=9009, log_level="info")
