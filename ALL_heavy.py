# Kill all Chrome processes.
CHROME_FLUSH_AFTER_CYCLES = 0
# Notify user the script is alive.
PING_AFTER_AMOUNT_OF_CYCLES = 1
# Wait this long between scrapes.
SECONDS_BETWEEN_SCRAPES = 5

# Choose the scraper modules to use:
BLIZZNEWS = 1
D3BLUE = 1
WOWBLUE = 1
WOWNEWS = 1

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

# Start Chrome webdrivers with all the options, for US and EU sites.
if D3BLUE or WOWBLUE == 1:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches',['enable-logging'])

# Check and import/prepare all flagged modules.
if D3BLUE == 1:
    import d3_blue
    us_full_page_d3 = webdriver.Chrome(options=options)
    eu_full_page_d3 = webdriver.Chrome(options=options)
if WOWBLUE == 1:
    import wow_blue
    us_full_page_wow = webdriver.Chrome(options=options)
    eu_full_page_wow = webdriver.Chrome(options=options)
if BLIZZNEWS == 1:
    import blizz_news
if WOWNEWS == 1:
    import wow_news

# Start the scraping loop.
scrapescounter = 0
while True:
    scrapescounter += 1
    if BLIZZNEWS == 1:
        blizz_news.scrape(PING_AFTER_AMOUNT_OF_CYCLES, scrapescounter,
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
    if D3BLUE == 1:
        d3_blue.scrape(0, PING_AFTER_AMOUNT_OF_CYCLES, scrapescounter, us_full_page_d3, eu_full_page_d3)
    if WOWBLUE == 1:
        wow_blue.scrape(0, PING_AFTER_AMOUNT_OF_CYCLES, scrapescounter, us_full_page_wow, eu_full_page_wow)
    if WOWNEWS == 1:
        wow_news.scrape(PING_AFTER_AMOUNT_OF_CYCLES, scrapescounter)

    # Restart the loop after a prescribed wait time.
    if SECONDS_BETWEEN_SCRAPES > 0:
        import time
        time.sleep(SECONDS_BETWEEN_SCRAPES)