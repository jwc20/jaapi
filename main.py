from fastapi import FastAPI, Request
from pprintpp import pprint

import os
from datetime import datetime

import LinkedInScraper
import WAASU # TODO

now = datetime.now()
date_time_format = now.strftime("%Y%m%d_%H%M%S")
output_filename = f"li_data_{date_time_format}.csv"


cwd = os.getcwd()
home_directory = "/home/cjw"
current_save_directory = "scraped_data"
current_save_directory = os.path.join(current_save_directory, "linkedin") # TODO: save for other job boards
save_filename = ""

if cwd != home_directory:
    cwd = home_directory
    os.chdir(cwd)

# TODO: save for other job boards
if os.path.exists(current_save_directory):
    save_filename = f"~/{current_save_directory}/{output_filename}"
else:
    os.makedirs(current_save_directory)
    save_filename = f"~/{current_save_directory}/{output_filename}"


app = FastAPI()


@app.post("/trigger")
async def post_cdio_json(request: Request):
    """
    trigger scraper when post request is received from cdio
    """
    pprint(request)
    
    req = await request.json()
    
    if "linkedin" in req.url:
        keyword = "software%20engineer"
        num_pages = 5
        print("Starting LinkedIn scraper.")
        scraped_jobs = LinkedInScraper.scrape_linkedin_jobs(keyword, num_pages)
        scraped_jobs.to_csv(save_filename, index=False)
        print("Ending LinkedIn scraper")

        
    
    # return await request.json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=9009, log_level="info")
