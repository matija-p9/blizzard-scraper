import code_by_diva
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import multiprocessing

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument('--log-level=3')
site_browser = webdriver.Chrome(options=options)


process1 = multiprocessing.Process(target=code_by_diva.scrape,args=(0, site_browser,)).start()
#process1 = multiprocessing.Process(target=code_by_diva.scrape,args=(1, site_browser,)).start()

process1.start()
#process2.start()

#code_by_diva.scrape(3, site_browser)