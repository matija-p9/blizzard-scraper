# Kill all Chrome processes.
CHROME_FLUSH_AFTER_CYCLES = 50
# Notify user the script is alive.
PING_AFTER_AMOUNT_OF_CYCLES = 1
# Wait this long between scrapes.
SECONDS_BETWEEN_SCRAPES = 5

# Track the following categories for Blizz_News (0 to untrack, ANY OTHER value to track):
BlizzCon = 1
Diablo_III = 1
Diablo_IV = 1
Call_of_Duty_Modern_Warfare = 1
Hearthstone = 1
Heroes_of_the_Storm = 1
Inside_Blizzard = 1
Overwatch = 1
StarCraft_II = 1
Warcraft_III_Reforged = 1
World_of_Warcraft = 1

# Import and prepare all dependencies for Blue tracking.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches',['enable-logging'])
import os
import time

def refresh_blue_wow():
    us_full_page_wow.set_page_load_timeout(60)
    us_full_page_wow.refresh()
    eu_full_page_wow.set_page_load_timeout(60)
    eu_full_page_wow.refresh()

def refresh_blue_d3():
    us_full_page_d3.set_page_load_timeout(60)
    us_full_page_d3.refresh()
    eu_full_page_d3.set_page_load_timeout(60)
    eu_full_page_d3.refresh()

# Start Chrome webdrivers with all the options, for US and EU sites.
us_full_page_wow = webdriver.Chrome(options=options)
eu_full_page_wow = webdriver.Chrome(options=options)
us_full_page_wow.get("https://us.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts")
eu_full_page_wow.get("https://eu.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts")
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
        refresh_blue_wow()
        refresh_blue_d3()
    except:
        os.system("TASKKILL /f  /IM  CHROME.EXE >NUL 2>&1")
        os.system("TASKKILL /f  /IM  CHROMEDRIVER.EXE >NUL 2>&1")
        us_full_page_wow = webdriver.Chrome(options=options)
        eu_full_page_wow = webdriver.Chrome(options=options)
        us_full_page_wow.get("https://us.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts")
        eu_full_page_wow.get("https://eu.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts")
        us_full_page_d3 = webdriver.Chrome(options=options)
        eu_full_page_d3 = webdriver.Chrome(options=options)
        us_full_page_d3.get("https://us.forums.blizzard.com/en/d3/g/blizzard-tracker/activity/posts")
        eu_full_page_d3.get("https://eu.forums.blizzard.com/en/d3/g/blizzard-tracker/activity/posts")
        try:
            refresh_blue_wow()
            refresh_blue_d3()
        except:
            continue
        continue

    #######################
    # B L I Z Z _ N E W S #
    #######################

    # Read the URL and dump it into a huge string.
    try:
        import urllib.request
        url_raw = urllib.request.urlopen("https://news.blizzard.com/en-us")
        mybytes = url_raw.read()
        mystr = mybytes.decode("utf8")
        url_raw.close()
    except:
        continue

    # Prepare parsing tools.
    linkStart = '<div class="ArticleListItem"><a href="'
    linkEnd = '"'
    postTitleStart = '<h3 class="ArticleListItem-title">'
    postTitleEnd = '</h3>'
    postDetailsStart = '<div class="h6">'
    postDetailsEnd = '</div>'
    categoryStart = '<div class="flush-top ArticleListItem-labelInner">'
    categoryEnd = '</div>'
    postLocations = []

    # Map useful scraped data for parsing.
    i, j = 0, 0
    while j < 100:
        if mystr.find(linkStart, i) + len(linkStart) < i:
            break
        postLocations.append(mystr.find(linkStart, i) + len(linkStart))
        i = mystr.find(linkStart, i) + len(linkStart)
        j += 1
    if j == 100: # Reset loop if the webdriver failed to load anything.
        continue

    # Store post information in a 2D array.
    # [x][y]
    # x : order of posts, 0 is newest
    # y : 0 = category, 1 = title, 2 = link, 3 = text
    post = []
    for loc in postLocations:
        # Category
        p = (mystr[mystr.find(categoryStart,loc)+len(categoryStart):mystr.find(categoryEnd,mystr.find(categoryStart,loc)+len(categoryStart))],
        # Title
        mystr[mystr.find(postTitleStart,loc)+len(postTitleStart):mystr.find(postTitleEnd,mystr.find(postTitleStart,loc)+len(postTitleStart))],
        # Link
        "https://news.blizzard.com" + mystr[loc:mystr.find(linkEnd,loc)],
        # Text
        mystr[mystr.find(postDetailsStart,loc)+len(postDetailsStart):mystr.find(postDetailsEnd,mystr.find(postDetailsStart,loc)+len(postDetailsStart))].strip())
        post.append(p)

    # Exclude posts from categories with value 0.
    excludeCategories = []
    if BlizzCon == 0:
        excludeCategories.append("BlizzCon")
    if Diablo_III == 0:
        excludeCategories.append("Diablo III")
    if Diablo_IV == 0:
        excludeCategories.append("Diablo IV")
    if Call_of_Duty_Modern_Warfare == 0:
        excludeCategories.append("Call of Duty: Modern Warfare")
    if Hearthstone == 0:
        excludeCategories.append("Hearthstone")
    if Heroes_of_the_Storm == 0:
        excludeCategories.append("Heroes of the Storm")
    if Inside_Blizzard == 0:
        excludeCategories.append("Inside Blizzard")
    if Overwatch == 0:
        excludeCategories.append("Overwatch")
    if StarCraft_II == 0:
        excludeCategories.append("StarCraft II")
    if Warcraft_III_Reforged == 0:
        excludeCategories.append("Warcraft III: Reforged")
    if World_of_Warcraft == 0:
        excludeCategories.append("World of Warcraft")

    # Write the scrape to a temporary file _blizz_blue_tmp.txt.
    f = open("_blizz_news_tmp.txt", "w")
    for i in range(len(post)):
        if post[i][0] in excludeCategories:
            continue
        f.write("\n")
        f.write(post[i][0])
        f.write("\n")
        f.write(post[i][1])
        f.write("\n")
        f.write(post[i][2])
        f.write("\n")
        f.write("\n")
    f.close()

    # Create _blizz_news.txt if it doesn't exist.
    try:
        tf = open("_blizz_news.txt", "r")
    except:
        tf = open("_blizz_news.txt", "w")
    tf.close()

    # Ping to console output that a scrape has been made.
    if scrapescounter % PING_AFTER_AMOUNT_OF_CYCLES == 0:
        print(time.asctime(time.localtime(time.time())), '--- ping --- blizz_news')

    import filecmp
    if filecmp.cmp("_blizz_news.txt", "_blizz_news_tmp.txt"):
        # No updates check and cleanup.
        os.remove("_blizz_news_tmp.txt")

    else:
        # Write changes to _wow_news.txt and _wow_news_recent.txt.
        import difflib
        text1 = open("_blizz_news.txt", errors='ignore', encoding='ascii').readlines()
        text2 = open("_blizz_news_tmp.txt", errors='ignore', encoding='ascii').readlines()

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
            changes = open("_blizz_news_recent.txt", "w")
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
        os.remove('_blizz_news.txt')
        os.rename('_blizz_news_tmp.txt', '_blizz_news.txt')

    #################
    # D 3 _ B L U E #
    #################

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

    ###################
    # W O W _ B L U E #
    ###################

    # Store data in raw_html.
    us_raw_html = str(us_full_page_wow.page_source)
    eu_raw_html = str(eu_full_page_wow.page_source)

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

    # Write the scrape to a temporary file _wow_blue_tmp.txt.
    f = open("_wow_blue_tmp.txt", "w+", errors='ignore')
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

    # Create _wow_blue.txt if it doesn't exist.
    try:
        tf = open("_wow_blue.txt", "r", errors='ignore')
    except:
        tf = open("_wow_blue.txt", "w", errors='ignore')
    tf.close()

    # Ping to console output that a scrape has been made.
    if scrapescounter % PING_AFTER_AMOUNT_OF_CYCLES == 0:
        print(time.asctime(time.localtime(time.time())), '--- ping --- wow_blue')

    import filecmp
    if filecmp.cmp("_wow_blue.txt", "_wow_blue_tmp.txt"):
        # No updates check and cleanup.
        os.remove("_wow_blue_tmp.txt")

    else:
        # Write changes to _wow_blue.txt and _wow_blue_recent.txt.
        import difflib
        text1 = open("_wow_blue.txt", errors='ignore', encoding='ascii').readlines()
        text2 = open("_wow_blue_tmp.txt", errors='ignore', encoding='ascii').readlines()
        changes = open("_wow_blue_recent.txt", "w")
        for line in difflib.unified_diff(text1, text2):
            if line.startswith('---') or line.startswith('+++'):
                continue
            elif line.startswith('-') or line.startswith('+'):
                changes.write(line[1:])
                print(line[1:], end='')

        # Clean up the files.
        os.remove('_wow_blue.txt')
        os.rename('_wow_blue_tmp.txt', '_wow_blue.txt')
        changes.close()

        # Alert user!
        import winsound
        winsound.PlaySound("sound.wav", winsound.SND_FILENAME)

    ###################
    # W O W _ N E W S #
    ###################

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

    # Write the scrape to a temporary file _wow_news_tmp.txt.
    nf = open("_wow_news_tmp.txt", "w")
    for location in titlelocations:
        nf.write('\n')
        nf.write(mystr[location:mystr.find(divclosestr, location)])
        nf.write('\n')
        nf.write("https://worldofwarcraft.com" + mystr[mystr.find(urlstr, location) + len(urlstr):mystr.find(urlclosestr, location)])
        nf.write('\n')
        nf.write('\n')
    nf.close()

    # Create _wow_news.txt if it doesn't exist.
    try:
        tf = open("_wow_news.txt", "r")
    except:
        tf = open("_wow_news.txt", "w")
    tf.close()

    # Ping to console output that a scrape has been made.
    if scrapescounter % PING_AFTER_AMOUNT_OF_CYCLES == 0:
        print(time.asctime(time.localtime(time.time())), '--- ping --- wow_news')

    import filecmp
    if filecmp.cmp("_wow_news.txt", "_wow_news_tmp.txt"):
        # No updates check and cleanup.
        os.remove("_wow_news_tmp.txt")

    else:
        # Write changes to _wow_news.txt and _wow_news_recent.txt.
        import difflib
        text1 = open("_wow_news.txt", errors='ignore', encoding='ascii').readlines()
        text2 = open("_wow_news_tmp.txt", errors='ignore', encoding='ascii').readlines()

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
                    i += 1
                    continue
        if diff > 0:

            # Write the changes.
            changes = open("_wow_news_recent.txt", "w")
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
        os.remove('_wow_news.txt')
        os.rename('_wow_news_tmp.txt', '_wow_news.txt')

    # Restart the loop after a prescribed wait time.
    if SECONDS_BETWEEN_SCRAPES > 0:
        time.sleep(SECONDS_BETWEEN_SCRAPES)