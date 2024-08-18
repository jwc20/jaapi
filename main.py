
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import os
from datetime import datetime
from pprintpp import pprint
import json

from li_scraper import LinkedInScraper
from li_scraper_db import LinkedInScraperDB
# import WAASU # TODO


from sqlalchemy import create_engine
import psycopg2
import dotenv

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

        if "watch_url" in message and "linkedin" in message["watch_url"]:
            keyword = "software%20engineer"
            num_pages = 5

            now = datetime.now()
            date_time_format = now.strftime("%Y%m%d_%H%M%S")
            # output_filename = f"li_data_{date_time_format}.csv"
            # print("Starting LinkedIn scraper.")
            # print(f"Filename: {output_filename}")

            print(date_time_format)
            # save_filename = f"./scraped_data/linkedin/{output_filename}"
            scraped_jobs = LinkedInScraperDB.scrape_linkedin_jobs(keyword, num_pages)
            # print(scraped_jobs)
            # scraped_jobs.to_csv(save_filename, index=False)

            try:
                conn_string = DATABASE_URL

                db = create_engine(conn_string)
                conn = db.connect()
                print("connected to postgres")
                # df = pd.DataFrame(data)
                scraped_jobs.to_sql(
                    "scraped_li_job_listings", con=conn, if_exists="replace", index=False
                )
                print("saved to postgres")
            except:
                print("I am unable to connect to the database")

            print("Ending LinkedIn scraper")

            # keyword = "software%20engineer"
            # num_pages = 5

            # now = datetime.now()
            # date_time_format = now.strftime("%Y%m%d_%H%M%S")
            # # output_filename = f"li_data_{date_time_format}.csv"
            # print(date_time_format)
            # print("Starting LinkedIn scraper.")
            # # print(f"Filename: {output_filename}")
            # # save_filename = f"/app/scraped_data/linkedin/{output_filename}"
            # scraped_jobs = LinkedInScraperDB.scrape_linkedin_jobs(keyword, num_pages)
            # # scraped_jobs.to_csv(save_filename, index=False)

            # print("Ending LinkedIn scraper")

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
