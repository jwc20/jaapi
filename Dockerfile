FROM python:3.11-slim


# RUN apt-get update \
#     && apt-get install -y curl unzip gnupg2 wget

# Install Chrome WebDriver
# RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
#     mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
#     unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     rm /tmp/chromedriver_linux64.zip && \
#     chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
#     ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# RUN wget -N http://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip -P ~/ \
#   && unzip ~/chromedriver_linux64.zip -d ~/ \
#   && rm ~/chromedriver_linux64.zip \
#   && mv -f ~/chromedriver /usr/local/bin/chromedriver \
#   && chown root:root /usr/local/bin/chromedriver \
#   && chmod 0755 /usr/local/bin/chromedriver

# run echo $PATH

# run which chromedriver

# Install Google Chrome
# RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
# echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
# apt-get -yqq update && \
# apt-get -yqq install google-chrome-stable && \
# rm -rf /var/lib/apt/lists/*


WORKDIR /app

RUN mkdir -p /app/scraped_data/linkedin


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9009

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9009", "--log-level", "info"]
