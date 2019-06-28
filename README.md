# Youtube Video Statistics Collector and API

# Usage

## Prerequisites

python>=3.7

Google API Key(Youtube Data API v3 Enabled)

## Install

$ pip install -r requirements.txt

$ python manage.py migrate

## Collect statistics

$ python manage.py update_videos *CHANNEL_ID* *GOOGLE_API_KEY1* # run this first to update video list.

$ python manage.py update_stats *CHANNEL_ID* *GOOGLE_API_KEY1*

## Run API server
$ python manage.py runserver
