FROM selenium/standalone-chrome:latest

# install python and pip
USER root
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /hack-alert

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# chrome-related environment variables
ENV CHROME_BINARY_LOCATION="/opt/google/chrome/chrome"
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"

CMD ["python3", "/hack-alert/slackbot.py"]