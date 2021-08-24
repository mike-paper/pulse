FROM python:3.9

# Update the package list and install chrome
# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get install -y libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1
ENV CHROME_VERSION 90.0.4430.212
# => was getting ERROR [ 6/18] RUN apt-get update -y && apt-get install -y google-chrome-stable=91.0.4472.164-1 
# upgraded to 92.0.4515.107, might need to downgrade to 91.0.4472.164 if something breaks in Slack
# RUN apt-get update -y && apt-get install -y google-chrome-stable=$CHROME_VERSION-1
# RUN apt-get install -y google-chrome-stable=$CHROME_VERSION-1

# Check available versions here: https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable
# ARG CHROME_VERSION="81.0.4044.113-1"
RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb \
  && apt install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION 90.0.4430.24
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH
# update config to not run as root
RUN sed -i 's|exec -a "$0" "$HERE/chrome" "$@"|exec -a "$0" "$HERE/chrome" "$@" --no-sandbox --user-data-dir |g' /opt/google/chrome/google-chrome

COPY requirements.txt /app/
RUN pip3 --default-timeout=600 install -r /app/requirements.txt

EXPOSE 22
EXPOSE 5000/tcp

ENV PORT 5000

COPY app.py /app/
COPY logger.py /app/
ADD pints /app/pints
ADD metrics /app/metrics
ADD static /app/static
ADD dbt /app/dbt

CMD cd app && exec gunicorn -t 900 --bind :$PORT --workers $WORKERS --threads 1 --preload app:app