#!/usr/bin/env python

import requests
import time
from datetime import datetime
import pandas as pd
import os
import json
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import psycopg2
import dotenv

dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

splash_url = "http://test.wonjchoi.com:8050/render.html"
extra_param = "f_E=1%2C2%2C3&f_TPR=r2592000&f_WT=2&f_TPR=r86400"

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
]


class LinkedInScraperDB:

    def __init__(self):
        pass

    @staticmethod
    def scrape_linkedin_jobs(keyword, num_pages):
        results = pd.DataFrame(
            columns=[
                "company_name",
                "job_title",
                # "extracted_skills",
                "job_link",
                # "job_description",
                # "date_scraped"
                "created_at",
                "updated_at",
            ]
        )

        for page in range(num_pages):
            keyword = "software%20engineer"
            extra_param = "f_E=1%2C2%2C3&f_TPR=r2592000&f_WT=2&f_TPR=r86400"
            url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&{extra_param}&start={page*25}"
            print(f"Scraping from: {url}")

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
                    "url": url,
                    "wait": 5,
                },
            )

            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.select(".base-card")

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

                    # job_description = LinkedInScraper.extract_job_description(job_link)
                    # extracted_skills = LinkedInScraper.extract_skills(job_description)

                    print(f"Job Title: {job_title}, Company: {company_name}")

                    results = results._append(
                        {
                            "company_name": company_name,
                            "job_title": job_title,
                            "job_link": job_link,
                            # "job_description": job_description,
                            # "extracted_skills": extracted_skills,
                            # "date_scraped": now,
                            "created_at": now,
                            "updated_at": now,
                        },
                        ignore_index=True,
                    )

                except Exception as e:
                    print(e)
                    continue

        return results

    @staticmethod
    def extract_job_description(job_link):
        lua_script = """P
        function main(splash, args)
            splash:go(args.url)
            splash:wait(5)
            local show_more = splash:select('.show-more-less-html__button')
            if show_more then
                show_more:click()
                splash:wait(2)
            end
            return splash:select('.description').text
        end
        """

        response = requests.post(
            splash_url,
            json={
                "lua_source": lua_script,
                "url": job_link,
                "wait": 5,
            },
        )

        job_description = response.text.strip()
        job_description = " ".join(job_description.split())
        return job_description

    @staticmethod
    def extract_skills(description):
        skills = [
            "PostgreSQL",
            "Airflow",
            "Python",
            "JavaScript",
            "TypeScript",
            "SQL",
            "Flask",
            "Django",
            "Nix",
            "React",
        ]
        description = description.lower()
        skills_list = [skill for skill in skills if skill.lower() in description]
        return skills_list

if __name__ == "__main__":
    keyword = "software%20engineer"
    num_pages = 5

    now = datetime.now()
    date_time_format = now.strftime("%Y%m%d_%H%M%S")
    output_filename = f"li_data_{date_time_format}.csv"
    # print("Starting LinkedIn scraper.")
    # print(f"Filename: {output_filename}")

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
