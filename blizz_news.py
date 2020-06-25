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

# Declare the function to call for wow_news scraping.
def scrape(PING_AFTER_AMOUNT_OF_CYCLES, scrapescounter,
          BlizzCon,
          Diablo_III,
          Diablo_IV,
          Call_of_Duty_Modern_Warfare,
          Hearthstone,
          Heroes_of_the_Storm,
          Inside_Blizzard,
          Overwatch,
          StarCraft_II,
          Warcraft_III_Reforged,
          World_of_Warcraft):

    import os
    import time
    import urllib.request
    import winsound

    # Read the URL and dump it into a huge string.
    try:
        url_raw = urllib.request.urlopen("https://news.blizzard.com/en-us")
        mybytes = url_raw.read()
        mystr = mybytes.decode("utf8")
        url_raw.close()
    except:
        return 1

    # Prepare parsing tools.
    linkStart = '<li class="ArticleListItem"><article><a href="'
    linkEnd = '"'
    postTitleStart = '<span class="sr-only">'
    postTitleEnd = '</span>'
    postDetailsStart = '<div class="h6">'
    postDetailsEnd = '</div>'
    categoryStart = '<small class="flush-top ArticleListItem-labelInner">'
    categoryEnd = '</small>'
    postLocations = []

    # Map useful scraped data for parsing.
    i, j = 0, 0
    while j < 100:
        if mystr.find(linkStart, i) + len(linkStart) < i:
            break
        postLocations.append(mystr.find(linkStart, i) + len(linkStart))
        i = mystr.find(linkStart, i) + len(linkStart)
        j += 1

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

    # Read/Open _blizz_news.txt file to check for new posts.
    links = []
    try:
        txtfile = open("_blizz_news.txt", errors='ignore', encoding='ascii').readlines()
        for line in txtfile:
            if line.startswith("https://news.blizzard.com"):
                links.append(line.strip())
    except:
        txtfile = open("_blizz_news.txt", "w")
        txtfile.close()
        txtfile = open("_blizz_news.txt", errors='ignore', encoding='ascii').readlines()

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

    # Ping to console output that a scrape has been made.
    if scrapescounter % PING_AFTER_AMOUNT_OF_CYCLES == 0:
        print(time.asctime(time.localtime(time.time())), '--- ping --- blizz_news')

    # Write changes to console and _blizz_news_tmp.txt file.
    newstuff = 0
    tmpfile = open("_blizz_news_tmp.txt", "w")
    for i in range(len(post)):
        if post [i][0] in excludeCategories:
            continue
        if post [i][2] in links:
            continue
        else:
            newstuff = 1
            print()
            print(post[i][0], "-", time.asctime(time.localtime(time.time())))
            print(post[i][1])
            print(post[i][2])
            tmpfile.write("\n")
            tmpfile.write(post[i][0])
            tmpfile.write(" - ")
            tmpfile.write(time.asctime(time.localtime(time.time())))        
            tmpfile.write("\n")
            tmpfile.write(post[i][1])
            tmpfile.write("\n")
            tmpfile.write(post[i][2])
            tmpfile.write("\n")
    tmpfile.close()

    # New posts on top, append old ones below.
    tmpfile = open("_blizz_news_tmp.txt", "a+")
    for line in txtfile:
        tmpfile.write(line)
    tmpfile.close()

    # Alert user with a sound.
    if newstuff == 1:
        winsound.PlaySound("sound.wav", winsound.SND_FILENAME)
        print()

    # Clean up the files.
    os.remove('_blizz_news.txt')
    os.rename('_blizz_news_tmp.txt', '_blizz_news.txt')

if __name__ == "__main__":

    # Start the scraping loop.
    scrapescounter = 0
    while True:
        scrapescounter += 1

        scrape(PING_AFTER_AMOUNT_OF_CYCLES, scrapescounter,
              BlizzCon,
              Diablo_III,
              Diablo_IV,
              Call_of_Duty_Modern_Warfare,
              Hearthstone,
              Heroes_of_the_Storm,
              Inside_Blizzard,
              Overwatch,
              StarCraft_II,
              Warcraft_III_Reforged,
              World_of_Warcraft)

        if SECONDS_BETWEEN_SCRAPES > 0:
            import time
            time.sleep(SECONDS_BETWEEN_SCRAPES)