# Notify user the script is alive.
PING_AFTER_AMOUNT_OF_CYCLES = 1
# Wait this long between scrapes.
SECONDS_BETWEEN_SCRAPES = 5

# Track the following categories (0 to untrack, ANY OTHER value to track):
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

import os
import time

# Start the scraping loop.
scrapescounter = 0
while True:
    scrapescounter += 1

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
        # Write changes to _blizz_news.txt and _blizz_news_recent.txt.
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
                    i += 1
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

    if SECONDS_BETWEEN_SCRAPES > 0:
        time.sleep(SECONDS_BETWEEN_SCRAPES)