import requests
#url of our Splash server, in this case localhost
# splash_url = "http://localhost:8050/render.png"
splash_url = "http://localhost:8050/render.html"
#url of the page we want to scrape
# target_url = "https://www.amazon.com/s?k=cool+stuff"
#params to tell Splash what to do

keyword = "software%20engineer"
extra_param = "f_E=1%2C2%2C3&f_TPR=r2592000&f_WT=2&f_TPR=r86400"
target_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&{extra_param}"



# https://www.linkedin.com/jobs/search/?keywords=software%20engineer&f_E=1%2C2%2C3&f_TPR=r2592000&f_WT=2&f_TPR=r86400

params = {
    #url we'd like to go to
    "url": target_url,
    #wait 2 seconds for JS rendering
    "wait": 5,
    }
#send the request to Splash server
response = requests.get(splash_url, params=params)
#write the response to a file
with open("splash-li.html", "wb") as file:
    file.write(response.content)
