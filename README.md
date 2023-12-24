# ShortsNotifier
A simple Python program that sends you a desktop notification the minute a youtube shorts video is posted by any of a specific list of channels

## Setup

1) Get a Youtube Data API 3 key and put it in `API_KEY.txt`

2) Run `pip install -r requirements.txt`

3)  Fill out `channel_ids.csv` so that the first element of each row is the channel ID of a YouTube channel (you can find it by looking at their channel description, pressing "Share channel" and then "Copy channel ID"). You can put the title of the channel after it (separated by a comma) to help remember which ID is which (it will be ignored)

![image](https://github.com/GrandTheftWalrus/ShortsNotifier/assets/70998757/b0437884-7375-470b-ba9d-2bc6279eeb1f)

4) Run it with `python ShortsNotifier.py` (it currently runs in a window that you just gotta ignore, unless you can hide the terminal or something)

## Notes/Todo

Note: The program uses 1 quota point per hour per channel you have, so if your API quota limit is 10,000 per day and you're running it 24/7 then you can only have 6 or 7 channels listed or else you'll run out of points. If you're running it like 8 or 16 hours a day then you can have 20 or 10 channels. I suppose you could also just decrease the rate at which it performs checks to increase the channel limit, too.

Todo: I think it actually notifies you of any video type, not just shorts. I'll fix dat soon

Todo: Make it run in the background/minimize to tray

Todo: Add scan rate as launch parameter
