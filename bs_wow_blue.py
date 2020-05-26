import blizzardscraper
import time



time_between_scrapes_in_seconds = 30
ping_after_this_many_scrapes = 1



ping = 0
while True:
    blizzardscraper.blue()
    blizzardscraper.wow()
    time.sleep(time_between_scrapes_in_seconds)
    ping += 1
    if ping % ping_after_this_many_scrapes == 0:
        print(time.asctime(time.localtime(time.time())), '--- ping')