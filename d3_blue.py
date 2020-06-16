# Kill all Chrome processes.
CHROME_FLUSH_AFTER_CYCLES = 0

# Notify user the script is alive.
PING_AFTER_AMOUNT_OF_CYCLES = 1

# Wait this long between scrapes.
SECONDS_BETWEEN_SCRAPES = 5

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches',['enable-logging'])
import os
import time

def refresh_blue_d3():
    us_full_page_d3.set_page_load_timeout(60)
    us_full_page_d3.refresh()
    eu_full_page_d3.set_page_load_timeout(60)
    eu_full_page_d3.refresh()

# Start Chrome webdrivers with all the options, for US and EU sites.
us_full_page_d3 = webdriver.Chrome(options=options)
eu_full_page_d3 = webdriver.Chrome(options=options)
us_full_page_d3.get("https://us.forums.blizzard.com/en/d3/g/blizzard-tracker/activity/posts")
eu_full_page_d3.get("https://eu.forums.blizzard.com/en/d3/g/blizzard-tracker/activity/posts")

# Start the scraping loop.
scrapescounter = 0
while True:
    scrapescounter += 1

    # Close all instances of Chrome and Chromedriver after CHROME_FLUSH_AFTER_CYCLES scrapes, to safeguard memory.
    if CHROME_FLUSH_AFTER_CYCLES > 0:
        if scrapescounter % CHROME_FLUSH_AFTER_CYCLES == 0:
            print("-----------------------------------------------")
            print(time.asctime(time.localtime(time.time())), '--- Flushing Chrome...')
            print("-----------------------------------------------")
            os.system("TASKKILL /f  /IM  CHROME.EXE >NUL 2>&1")
            os.system("TASKKILL /f  /IM  CHROMEDRIVER.EXE >NUL 2>&1")

    # Open Chrome, read the pages, or refresh existing instance of webdriver.
    try:
        refresh_blue_d3()
    except:
        os.system("TASKKILL /f  /IM  CHROME.EXE >NUL 2>&1")
        os.system("TASKKILL /f  /IM  CHROMEDRIVER.EXE >NUL 2>&1")
        us_full_page_d3 = webdriver.Chrome(options=options)
        eu_full_page_d3 = webdriver.Chrome(options=options)
        us_full_page_d3.get("https://us.forums.blizzard.com/en/d3/g/blizzard-tracker/activity/posts")
        eu_full_page_d3.get("https://eu.forums.blizzard.com/en/d3/g/blizzard-tracker/activity/posts")
        try:
            refresh_blue_d3()
        except:
            continue
        continue
    
    # Store data in raw_html.
    us_raw_html = str(us_full_page_d3.page_source)
    eu_raw_html = str(eu_full_page_d3.page_source)

    # Define variables for parsing purposes.
    us_link_loc = []
    eu_link_loc = []
    link_beg = '<a href="/en/d3/t/'
    link_end = '">'
    time_data = 'data-time="'
    timestamp_beg = 'date date" title="'
    timestamp_end = '"'
    content_beg_beg = '<div class="group-post-excerpt distinguished-text-marking distinguished-text-marking--'
    content_beg_end = '">'
    content_end = '</div>'

    # Find locations of relevant links on the page.
    i, j = 0, 0
    while j < 50:
        if us_raw_html.find(link_beg, i) + len(link_beg) < i:
            break
        us_link_loc.append(us_raw_html.find(link_beg, i) + len(link_beg))
        i = us_raw_html.find(link_beg, i) + len(link_beg)
        j += 1
    if j == 50: # Reset loop if the webdriver failed to load anything.
        continue
    i, j = 0, 0
    while j < 50:
        if eu_raw_html.find(link_beg, i) + len(link_beg) < i:
            break
        eu_link_loc.append(eu_raw_html.find(link_beg, i) + len(link_beg))
        i = eu_raw_html.find(link_beg, i) + len(link_beg)
        j += 1
    if j == 50: # Reset loop if the webdriver failed to load anything.
        continue

    # Store post information in a 2D array.
    # [x][y]
    # x : order of posts, 0 is newest
    # y : 0 = timedata, 1 = timestamp, 2 = title, 3 = link, 4 = text
    post = []
    for loc in us_link_loc:
        # Timedata
        p = (us_raw_html[us_raw_html.find(time_data,loc)+len(time_data):us_raw_html.find('"',us_raw_html.find(time_data,loc)+len(time_data))],
        # Timestamp
        "US - "+us_raw_html[us_raw_html.find(timestamp_beg,loc)+len(timestamp_beg):us_raw_html.find(timestamp_end,us_raw_html.find(timestamp_beg,loc)+len(timestamp_beg))],
        # Post title
        us_raw_html[us_raw_html.find(link_end,loc)+2:us_raw_html.find("</a>",loc)],
        # Post link
        "https://us.forums.blizzard.com/en/d3/t/" + us_raw_html[loc:us_raw_html.find(link_end,loc)],
        # Post text
        us_raw_html[us_raw_html.find(content_beg_end,us_raw_html.find(content_beg_beg,loc))+2:
        us_raw_html.find(content_end,us_raw_html.find(content_beg_end,us_raw_html.find(content_beg_beg,loc)))].replace("\n",""))
        post.append(p)
    for loc in eu_link_loc:
        # Timedata
        p = (eu_raw_html[eu_raw_html.find(time_data,loc)+len(time_data):eu_raw_html.find('"',eu_raw_html.find(time_data,loc)+len(time_data))],
        # Timestamp
        "EU - "+eu_raw_html[eu_raw_html.find(timestamp_beg,loc)+len(timestamp_beg):eu_raw_html.find(timestamp_end,eu_raw_html.find(timestamp_beg,loc)+len(timestamp_beg))],
        # Post title
        eu_raw_html[eu_raw_html.find(link_end,loc)+2:eu_raw_html.find("</a>",loc)],
        # Post link
        "https://eu.forums.blizzard.com/en/d3/t/" + eu_raw_html[loc:eu_raw_html.find(link_end,loc)],
        # Post text
        eu_raw_html[eu_raw_html.find(content_beg_end,eu_raw_html.find(content_beg_beg,loc))+2:
        eu_raw_html.find(content_end,eu_raw_html.find(content_beg_end,eu_raw_html.find(content_beg_beg,loc)))].replace("\n",""))
        post.append(p)
    post.sort(reverse=True)

    # Write the scrape to a temporary file _d3_blue_tmp.txt.
    f = open("_d3_blue_tmp.txt", "w+", errors='ignore')
    for i in range(len(post)):
        f.write("\n")
        f.write(post[i][1] + " - " + post[i][2])
        f.write("\n")
        f.write(post[i][3])
        f.write("\n")
        f.write("\n" + post[i][4].strip())
        f.write("\n")
        f.write("\n")
    f.close()

    # Create _d3_blue.txt if it doesn't exist.
    try:
        tf = open("_d3_blue.txt", "r", errors='ignore')
    except:
        tf = open("_d3_blue.txt", "w", errors='ignore')
    tf.close()

    # Ping to console output that a scrape has been made.
    if scrapescounter % PING_AFTER_AMOUNT_OF_CYCLES == 0:
        print(time.asctime(time.localtime(time.time())), '--- ping --- d3_blue')

    import filecmp
    if filecmp.cmp("_d3_blue.txt", "_d3_blue_tmp.txt"):
        # No updates check and cleanup.
        os.remove("_d3_blue_tmp.txt")

    else:
        # Write changes to _d3_blue.txt and _d3_blue_recent.txt.
        import difflib
        text1 = open("_d3_blue.txt", errors='ignore', encoding='ascii').readlines()
        text2 = open("_d3_blue_tmp.txt", errors='ignore', encoding='ascii').readlines()
        changes = open("_d3_blue_recent.txt", "w")
        for line in difflib.unified_diff(text1, text2):
            if line.startswith('---') or line.startswith('+++'):
                continue
            elif line.startswith('-') or line.startswith('+'):
                changes.write(line[1:])
                print(line[1:], end='')

        # Clean up the files.
        os.remove('_d3_blue.txt')
        os.rename('_d3_blue_tmp.txt', '_d3_blue.txt')
        changes.close()

        # Alert user!
        import winsound
        winsound.PlaySound("sound.wav", winsound.SND_FILENAME)

    if SECONDS_BETWEEN_SCRAPES > 0:
        time.sleep(SECONDS_BETWEEN_SCRAPES)