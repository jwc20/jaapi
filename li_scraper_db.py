#!/usr/bin/env python

import requests
from datetime import datetime
import pandas as pd
import os
from bs4 import BeautifulSoup
import sqlalchemy
import dotenv

from collections import namedtuple

dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

splash_url = "http://test.wonjchoi.com:8050/render.html"

now = datetime.now()

ignore_companies = [
    "minware",
    "HireMeFast LLC",
    "SynergisticIT",
    "Get It Recruit - Information Technology",
    "Team Remotely Inc",
    "Dice",
    "Actalent",
    "Patterned Learning Career",
    "Sky Recruitment LLC",
    "Fitness Matrix Inc",
    "Outco Inc",
    "HireMeFast",
    "Phoenix Recruitment",
    "TEKsystems",
    "RemoteWorker US",
    "Accenture Federal Services",
    "Jobot",
    "Crossover",
    "Esyconnect",
    "RemoteWorker UK",
    "Jobot Consulting",
    "Team Remotely",
]

Data = namedtuple("Data", ["count", "results"])


class LinkedInScraperDB:

    def __init__(self):
        pass

    @staticmethod
    def scrape_linkedin_jobs(url_to_scrape, num_pages):
        number_of_jobs = 0
        
        
        results = pd.DataFrame(
            columns=[
                "company_name",
                "job_title",
                "job_link",
                "created_at",
                "updated_at",
                "source",
                "scraped_from"
            ]
        )

        for _ in range(num_pages):
            print(f"Scraping from: {url_to_scrape}")

            lua_script = """
            function main(splash, args)
                splash:go(args.url)
                splash:wait(5)
                splash:scroll_to(splash:jq('.jobs-search-results-list')[0])
                splash:wait(2)
                return splash:html()
            end
            """

            response = requests.post(
                splash_url,
                json={
                    "lua_source": lua_script,
                    "url": url_to_scrape,
                    "wait": 5,
                },
            )

            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.select(".base-card")
            
            number_of_jobs += len(job_cards)

            for card in job_cards:
                try:
                    job_title_element = card.select_one(".base-search-card__title")
                    company_element = card.select_one(".base-search-card__subtitle")
                    description_element = card.select_one(".base-card__full-link")
                    company_name = company_element.text.strip()

                    if company_name.lower() in list(map(str.lower, ignore_companies)):
                        continue

                    job_title = job_title_element.text.strip()
                    job_link = description_element["href"]

                    # print(f"Job Title: {job_title}, Company: {company_name}")

                    # TODO: remove jobs with null values

                    results = results._append(
                        {
                            "company_name": company_name,
                            "job_title": job_title,
                            "job_link": job_link,
                            "created_at": now,
                            "updated_at": now,
                            "source": "linkedin",
                            "scraped_from" : url_to_scrape,
                        },
                        ignore_index=True,
                    )

                except Exception as e:
                    print(e)
                    continue

        return Data(number_of_jobs, results)
