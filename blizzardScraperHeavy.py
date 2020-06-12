# Kill all Chrome processes.
CHROME_FLUSH_AFTER_CYCLES = 20

# Notify user the script is alive.
PING_AFTER_AMOUNT_OF_CYCLES = 1

# Wait this long between scrapes.
SECONDS_BETWEEN_SCRAPES = 0

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches',['enable-logging'])
import os
import time

def refresh_blue_pages():
    us_full_page.set_page_load_timeout(60)
    us_full_page.refresh()
    eu_full_page.set_page_load_timeout(60)
    eu_full_page.refresh()

# Start Chrome webdrivers with all the options, for US and EU sites.
us_full_page = webdriver.Chrome(options=options)
eu_full_page = webdriver.Chrome(options=options)
us_full_page.get("https://us.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts")
eu_full_page.get("https://eu.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts")

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
        refresh_blue_pages()
    except:
        os.system("TASKKILL /f  /IM  CHROME.EXE >NUL 2>&1")
        os.system("TASKKILL /f  /IM  CHROMEDRIVER.EXE >NUL 2>&1")
        us_full_page = webdriver.Chrome(options=options)
        eu_full_page = webdriver.Chrome(options=options)
        us_full_page.get("https://us.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts")
        eu_full_page.get("https://eu.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts")
        try:
            refresh_blue_pages()
        except:
            continue
        continue
    
    # Store data in raw_html.
    us_raw_html = str(us_full_page.page_source)
    eu_raw_html = str(eu_full_page.page_source)

    # Define variables for parsing purposes.
    us_link_loc = []
    eu_link_loc = []
    link_beg = '<a href="/en/wow/t/'
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
        "https://us.forums.blizzard.com/en/wow/t/" + us_raw_html[loc:us_raw_html.find(link_end,loc)],
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
        "https://eu.forums.blizzard.com/en/wow/t/" + eu_raw_html[loc:eu_raw_html.find(link_end,loc)],
        # Post text
        eu_raw_html[eu_raw_html.find(content_beg_end,eu_raw_html.find(content_beg_beg,loc))+2:
        eu_raw_html.find(content_end,eu_raw_html.find(content_beg_end,eu_raw_html.find(content_beg_beg,loc)))].replace("\n",""))
        post.append(p)
    post.sort(reverse=True)

    # Write the scrape to a temporary file temp_blue.txt.
    f = open("temp_blue.txt", "w+", errors='ignore')
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

    # Create data_blue.txt if it doesn't exist.
    try:
        tf = open("data_blue.txt", "r", errors='ignore')
    except:
        tf = open("data_blue.txt", "w", errors='ignore')
    tf.close()

    # Ping to console output that a scrape has been made.
    if scrapescounter % PING_AFTER_AMOUNT_OF_CYCLES == 0:
        print(time.asctime(time.localtime(time.time())), '--- ping --- BLUE POSTS')

    import filecmp
    if filecmp.cmp("data_blue.txt", "temp_blue.txt"):
        # No updates check and cleanup.
        os.remove("temp_blue.txt")

    else:
        # Write changes to data_blue.txt and data_blue_changes.txt.
        import difflib
        text1 = open("data_blue.txt", errors='ignore', encoding='ascii').readlines()
        text2 = open("temp_blue.txt", errors='ignore', encoding='ascii').readlines()
        changes = open("data_blue_changes.txt", "a")
        changes.write('----------')
        for line in difflib.unified_diff(text1, text2):
            if line.startswith('---') or line.startswith('+++'):
                continue
            elif line.startswith('-') or line.startswith('+'):
                changes.write(line[1:])
                print(line[1:], end='')

        # Clean up the files.
        os.remove('data_blue.txt')
        os.rename('temp_blue.txt', 'data_blue.txt')
        changes.close()

        # Alert user!
        import winsound
        winsound.PlaySound("sound.wav", winsound.SND_FILENAME)
    
    """
    WORLDOFWARCRAFT.COM NEWS SCRAPER
    """

    # Read the URL and dump it into a huge string.
    try:
        import urllib.request
        url_raw = urllib.request.urlopen("https://worldofwarcraft.com/en-us/news")
        mybytes = url_raw.read()
        mystr = mybytes.decode("utf8")
        url_raw.close()
    except:
        continue

    # Prepare parsing tools.
    titlestr = 'NewsBlog-title">'
    divclosestr = '</div>'
    urlstr = 'NewsBlog-link" href="'
    urlclosestr = '"></a></article></div>'
    titlelocations = []

    # Map useful scraped data for parsing.
    i, j = 0, 0
    while j < 150:
        if mystr.find(titlestr, i) + len(titlestr) < i:
            break
        titlelocations.append(mystr.find(titlestr, i) + len(titlestr))
        i = mystr.find(titlestr, i) + len(titlestr)
        j += 1
    if j == 150: # Reset loop if the webdriver failed to load anything.
        continue

    # Write the scrape to a temporary file temp_wow_com.txt.
    nf = open("temp_wow_com.txt", "w")
    for location in titlelocations:
        nf.write('\n')
        nf.write(mystr[location:mystr.find(divclosestr, location)])
        nf.write('\n')
        nf.write("https://worldofwarcraft.com" + mystr[mystr.find(urlstr, location) + len(urlstr):mystr.find(urlclosestr, location)])
        nf.write('\n')
        nf.write('\n')
    nf.close()

    # Create data_wow_com.txt if it doesn't exist.
    try:
        tf = open("data_wow_com.txt", "r")
    except:
        tf = open("data_wow_com.txt", "w")
    tf.close()

    # Ping to console output that a scrape has been made.
    if scrapescounter % PING_AFTER_AMOUNT_OF_CYCLES == 0:
        print(time.asctime(time.localtime(time.time())), '--- ping --- WOW.com NEWS')

    import filecmp
    if filecmp.cmp("data_wow_com.txt", "temp_wow_com.txt"):
        # No updates check and cleanup.
        os.remove("temp_wow_com.txt")

    else:
        # Write changes to data_wow_com.txt and data_wow_com_changes.txt.
        import difflib
        text1 = open("data_wow_com.txt", errors='ignore', encoding='ascii').readlines()
        text2 = open("temp_wow_com.txt", errors='ignore', encoding='ascii').readlines()

        # Double-check to fix the bug of old data being reported as new:
        # https://github.com/matija-p9/blizzard-scraper/issues/1
        diff = 1
        if len(text1) > 0:
            diff, i = 0, 0
            while i < len(text1):
                falsediff = 0
                try:
                    if text1[i] != text2[i]:
                        for j in range(len(text1)):
                            if text1[i] == text2[j]:
                                falsediff = 1
                        if falsediff == 0:
                            diff += 1
                    i += 1
                except:
                    diff += 1
                    continue
        if diff > 0:

            # Write the changes.
            changes = open("data_wow_com_changes.txt", "a")
            changes.write('\n')
            changes.write(time.asctime(time.localtime(time.time())))
            changes.write('\n\n')
            for line in difflib.unified_diff(text1, text2):
                if line.startswith('---') or line.startswith('+++'):
                    continue
                elif line.startswith('-') or line.startswith('+'):
                    changes.write(line[1:])
                    print(line[1:], end='')
            changes.close()

            # Alert user!
            import winsound
            winsound.PlaySound("sound.wav", winsound.SND_FILENAME)

        # Clean up the files.
        os.remove('data_wow_com.txt')
        os.rename('temp_wow_com.txt', 'data_wow_com.txt')

    if SECONDS_BETWEEN_SCRAPES > 0:
        time.sleep(SECONDS_BETWEEN_SCRAPES)