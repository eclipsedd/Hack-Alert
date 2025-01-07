FROM python:3.12-slim

WORKDIR /hack-alert

# dependencies for Chrome, chromedriver, and xvfb
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    xvfb \
    xauth \
    libxi6 \
    libgconf-2-4 \
    libxrender1 \
    libxtst6 \
    libnss3 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Chrome & chromedriver
RUN wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome.deb || apt-get -fy install && \
    rm google-chrome.deb

RUN CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Ensure chromedriver is executable
RUN chmod +x /usr/local/bin/chromedriver

COPY requirements.txt /hack-alert/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /hack-alert

# Set environment variable for headless Chrome
ENV DISPLAY=:99

CMD ["xvfb-run", "python3", "/hack-alert/slackbot.py"]