import os
import time
from selenium import webdriver
import datetime
import base64
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import matplotlib.pyplot as plt
import winsound
import threading

#-----------------------------
# test page ------------> i=0
# d3_blue_us -----------> i=1
# d3_blue_eu -----------> i=2
# wow_blue_us ----------> i=3
# wow_blue_eu ----------> i=4
#-----------------------------
#################################################
# Prerequired files: filemine_for_news0.txt, 
#                        filemine_for_news1.txt,
#                        filemine_for_news2.txt
#                        filemine_for_news3.txt
#                        filemine_for_news4.txt
# in ../User/username
#################################################   

# global variables managed by user

DELAY = 10
OUTPUT_SECOND_DEVIDED_BY = 15
PICTURE_DURATION = 2
FOLDER_PATH = "C://Users/Iva Vrsaljko/"

# Lists of elements needed to scrape sites

first_post_selector=".user-stream > div > div:nth-child(1)"
last_update = ".user-stream > div > div:nth-child(1) > div:nth-child(7) > span"
title_selector = ".user-stream > div > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)"
text_selector = ".user-stream > div > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > div:nth-child(1)"
SITES_TO_SCRAPE = ["http://stylemyweb.net/", "https://us.forums.blizzard.com/en/d3/g/blizzard-tracker/activity/posts", "https://eu.forums.blizzard.com/en/d3/g/blizzard-tracker/activity/posts", "https://us.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts", "https://eu.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts"]
SITE_NAME = ["test_site", "d3_blue_us", "d3_blue_eu", "wow_blue_us", "wow_blue_eu"]
LAST_UPDATE_SELECTOR = [".skip-link", last_update, last_update, last_update, last_update]
FIRST_POST_CSS_SELECTOR = [".entry-title", first_post_selector, first_post_selector, first_post_selector, first_post_selector]
TITLE_CSS_SELECTOR = [".entry-title", title_selector, title_selector, title_selector, title_selector]
TEXT_CSS_SELECTOR = ["body", text_selector, text_selector, text_selector, text_selector]

def scrape(i, site_browser):
        index = i
        site_browser.get(SITES_TO_SCRAPE[index])
        look_for_change(index, site_browser)

def is_page_loaded(index, site_browser):
        try:
            WebDriverWait(site_browser, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, TITLE_CSS_SELECTOR[index])))
            # This if is used just to get less print statements at the end
            if ((datetime.datetime.now().second % OUTPUT_SECOND_DEVIDED_BY) == 0):
                print(datetime.datetime.now(), 'Page ------------', SITE_NAME[index] , "------------ Last update was:",  str(site_browser.find_element_by_css_selector(LAST_UPDATE_SELECTOR[index]).text))
        except TimeoutException:
            print ("Loading took too much time so I made a sound!")
            winsound.PlaySound("sound.wav", winsound.SND_FILENAME)
            return True

def change_on_site(index, site_browser):
    # Alert user!
    winsound.PlaySound("sound.wav", winsound.SND_FILENAME)
    # Clear console and print the last post
    clear = lambda: os.system('cls')
    clear()
    print ("#######################################################################")
    print (site_browser.find_element_by_css_selector(TITLE_CSS_SELECTOR[index]).text)
    print ("#######################################################################")
    print ("#######################################################################")
    print ((site_browser.find_element_by_css_selector(TEXT_CSS_SELECTOR[index]).text)[0:500])
    print ("#######################################################################")
    print ((site_browser.find_element_by_css_selector(TITLE_CSS_SELECTOR[index]).get_attribute("href")))
    print ("#######################################################################")
    # Push notif in the form of a picture
    fig = plt.figure()
    fig.text(0.1, 0.9, site_browser.find_element_by_css_selector(TITLE_CSS_SELECTOR[index]).text, bbox=dict(facecolor='red', alpha=0.5))
    fig.text(0.1, 0.6, (site_browser.find_element_by_css_selector(TEXT_CSS_SELECTOR[index]).text)[0:500], bbox=dict(facecolor='red', alpha=0.5))
    fig.text(0.1, 0.3, site_browser.find_element_by_css_selector(TITLE_CSS_SELECTOR[index]).get_attribute("href"), bbox=dict(facecolor='red', alpha=0.5))
    plt.show(block=False)
    plt.pause(PICTURE_DURATION)
    plt.close()

def look_for_change(index, site_browser):
    while True:
        with open(FOLDER_PATH + SITE_NAME[index] + '.txt', 'r') as f:
            older_source = f.read()
            f.close()
        site_browser.refresh()
        is_page_loaded(index, site_browser)
        try:
            newer_source = site_browser.find_element_by_css_selector(TEXT_CSS_SELECTOR[index]).text
            if newer_source != older_source:
                with open(FOLDER_PATH + SITE_NAME[index] + '.txt', 'w') as f:
                    f.write(newer_source)
                    f.close()
                change_on_site(index, site_browser)
        except:
            print("!")


if __name__ == "__main__":

    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    site_browser = webdriver.Chrome(options=options)
    i=0


    scrape(i, site_browser)

