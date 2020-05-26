def wow():

    # Read the URL and dump it into a huge string.
    try:
        import urllib.request
        url_raw = urllib.request.urlopen("https://worldofwarcraft.com/en-us/news")
        mybytes = url_raw.read()
        mystr = mybytes.decode("utf8")
        url_raw.close()
    except:
        print("unable to connect to worldofwarcraft.com...")
        return

    # Prepare parsing tools.
    titlestr = 'NewsBlog-title">'
    divclosestr = '</div>'
    urlstr = 'NewsBlog-link" href="'
    urlclosestr = '"></a></div>'
    titlelocations = []

    # Map useful scraped data for parsing.
    i = 0
    while True:
        if mystr.find(titlestr, i) + 16 < i:
            break
        titlelocations.append(mystr.find(titlestr, i) + 16)
        i = mystr.find(titlestr, i) + 16

    # Write the scrape to a temporary file newdata.txt.
    nf = open("wownewdata.txt", "w")
    for location in titlelocations:
        nf.write(mystr[location:mystr.find(divclosestr, location)])
        nf.write('\n')
        nf.write("https://worldofwarcraft.com" + mystr[mystr.find(urlstr, location) + 21:mystr.find(urlclosestr, location)])
        nf.write('\n')
        nf.write('\n')
    nf.close()

    # Create wow_data.txt if it doesn't exist.
    try:
        tf = open("wow_data.txt", "r")
    except:
        tf = open("wow_data.txt", "w")
    tf.close()

    import filecmp
    import os
    if filecmp.cmp("wow_data.txt", "wownewdata.txt"):
        # No updates check and cleanup.
        os.remove("wownewdata.txt")
    else:
        import difflib
        import time

        # Write changes to wow_data.txt and wow_changelog.txt.
        text1 = open("wow_data.txt", errors='ignore').readlines()
        text2 = open("wownewdata.txt", errors='ignore').readlines()
        changes = open("wow_changelog.txt", "a")
        changes.write('\n')
        changes.write(time.asctime(time.localtime(time.time())))
        changes.write('\n\n')
        for line in difflib.unified_diff(text1, text2):
            if line.startswith('---') or line.startswith('+++'):
                continue
            elif line.startswith('-') or line.startswith('+'):
                changes.write(line[1:])
                print(line[1:], end='')

        # Clean up the files.
        os.remove('wow_data.txt')
        os.rename('wownewdata.txt', 'wow_data.txt')
        changes.close()

        # Alert user!
        import winsound
        winsound.PlaySound("sound.wav", winsound.SND_FILENAME)


def blue():

    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options

    # Start webdriver, open Firefox, read the page, store it in raw_html.
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    us_full_page = webdriver.Firefox(options=firefox_options)
    us_full_page.get('https://us.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts')
    us_raw_html = str(us_full_page.page_source)
    eu_full_page = webdriver.Firefox(options=firefox_options)
    eu_full_page.get('https://eu.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/posts')
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
    i = 0
    while True:
        if us_raw_html.find(link_beg, i) + len(link_beg) < i:
            break
        us_link_loc.append(us_raw_html.find(link_beg, i) + len(link_beg))
        i = us_raw_html.find(link_beg, i) + len(link_beg)
    i = 0
    while True:
        if eu_raw_html.find(link_beg, i) + len(link_beg) < i:
            break
        eu_link_loc.append(eu_raw_html.find(link_beg, i) + len(link_beg))
        i = eu_raw_html.find(link_beg, i) + len(link_beg)

    # Store post information in a 2D array.
    # [x][y]
    #   x : order of posts, 0 is newest
    #   y : 0 = timedata, 1 = timestamp, 2 = title, 3 = link, 4 = text
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

    # Close and shut down webdriver to avoid memory leaks.
    us_full_page.stop_client()
    us_full_page.quit()
    eu_full_page.stop_client()
    eu_full_page.quit()

    # Write the scrape to a temporary file bluenewdata.txt.
    f = open("bluenewdata.txt", "w+", errors='ignore')
    for i in range(len(post)):
        f.write("\n")
        f.write(post[i][1] + " - " + post[i][2])
        f.write("\n")
        f.write("\n" + post[i][3])
        f.write("\n")
        f.write("\n" + post[i][4].strip())
        f.write("\n")
        f.write("\n")
    f.close()

    # Create blue_data.txt if it doesn't exist.
    try:
        tf = open("blue_data.txt", "r", errors='ignore')
    except:
        tf = open("blue_data.txt", "w", errors='ignore')
    tf.close()

    import filecmp
    import os
    if filecmp.cmp("blue_data.txt", "bluenewdata.txt"):
        # No updates check and cleanup.
        os.remove("bluenewdata.txt")
    else:
        import difflib

        # Write changes to blue_data.txt and blue_changelog.txt.
        text1 = open("blue_data.txt", errors='ignore').readlines()
        text2 = open("bluenewdata.txt", errors='ignore').readlines()
        changes = open("blue_changelog.txt", "a")
        changes.write('----------')
        for line in difflib.unified_diff(text1, text2):
            if line.startswith('---') or line.startswith('+++'):
                continue
            elif line.startswith('-') or line.startswith('+'):
                changes.write(line[1:])
                print(line[1:], end='')

        # Clean up the files.
        os.remove('blue_data.txt')
        os.rename('bluenewdata.txt', 'blue_data.txt')
        changes.close()

        # Alert user!
        import winsound
        winsound.PlaySound("sound.wav", winsound.SND_FILENAME)
