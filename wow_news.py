# Notify user the script is alive.
PING_AFTER_AMOUNT_OF_CYCLES = 1
# Wait this long between scrapes.
SECONDS_BETWEEN_SCRAPES = 5

# Declare the function to call for wow_news scraping.
def scrape(PING_AFTER_AMOUNT_OF_CYCLES, scrapescounter):

    import os
    import time
    # Read the URL and dump it into a huge string.
    try:
        import urllib.request
        url_raw = urllib.request.urlopen("https://worldofwarcraft.com/en-us/news")
        mybytes = url_raw.read()
        mystr = mybytes.decode("utf8")
        url_raw.close()
    except:
        return 1

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
        return 1

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
                    continue
        if diff > 0:

            # Write the changes.
            for line in difflib.unified_diff(text1, text2):
                if line.startswith('---') or line.startswith('+++'):
                    continue
                elif line.startswith('-') or line.startswith('+'):
                    print(line[1:], end='')

            # Clean up the files.
            os.remove('_wow_news.txt')
            os.rename('_wow_news_tmp.txt', '_wow_news.txt')

            # Alert user!
            import winsound
            winsound.PlaySound("sound.wav", winsound.SND_FILENAME)

if __name__ == "__main__":

    # Start the scraping loop.
    scrapescounter = 0
    while True:
        scrapescounter += 1

        scrape(PING_AFTER_AMOUNT_OF_CYCLES, scrapescounter)

        if SECONDS_BETWEEN_SCRAPES > 0:
            import time
            time.sleep(SECONDS_BETWEEN_SCRAPES)