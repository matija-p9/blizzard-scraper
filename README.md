# Blizzard Scraper - Blue posts & News
Python3 script for reading and reporting content updates from World of Warcraft official sources

---
## Information
The script checks these pages for updates, periodically:
- https://news.blizzard.com/en-us - Blizzard News
- https://us.forums.blizzard.com/en/d3/g/blizzard-tracker/activity/posts
- https://eu.forums.blizzard.com/en/d3/g/blizzard-tracker/activity/posts - Diablo 3 Blue posts
- https://us.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts
- https://eu.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts - WoW Blue posts
- https://www.worldofwarcraft.com/en-us/news/ - WoW News

When a change is detected, it's written in the console window, as well as corresponding .txt files.

---
## Setup
To run the script, you need the following setup on your machine:
- Install Python3 - https://www.python.org/
- Install Selenium library - https://pypi.org/project/selenium/
- Extract Chrome Webdriver - https://sites.google.com/a/chromium.org/chromedriver/downloads

With that done, edit ALL_heavy.py with a text editor to customize it before running. First three lines of code are variables:
- CHROME_FLUSH_AFTER_CYCLES - amount of scrapes the script does before resetting Chrome completely. Useful to ensure no long-runtime memory leaks. 0 to switch off.
- PING_AFTER_AMOUNT_OF_CYCLES - amount of scrapes the script does before notifying the user in the console.
- SECONDS_BETWEEN_SCRAPES - how long should the script wait between two scrapes. It takes 3-4 seconds on average, without waiting.
---
Run ALL_heavy.py.
You can optionally run individual source scripts: blizz_news.py, d3_blue.py, wow_blue.py, wow_news.py.
