import pandas as pd 
import csv
import selenium 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.action_chains import ActionChains
import logging
import time
import csv
import datetime as datetime
import os

########################################
# Helper methods
########################################

user = 'jzruthh_7' # set user for your own computer
login = False
searchTerm = ['Sigma']
lengthOfScroll = 1

def startBrowser():
    options = webdriver.ChromeOptions()
    userdatadir = f'/Users/{user}/Desktop/TikTok/Chrome/'
    profile = 'Profile 1'
    options.add_argument(f"--user-data-dir={userdatadir}")
    options.add_argument(f"--profile-directory={profile}")
    browser = webdriver.Chrome(options=options)
    logging.info("Opening browser!")
    browser.get("https://www.tiktok.com")
    if (login):
        time.sleep(100)
    else:
        time.sleep(1)
    return browser


def downloadPage(browser, filePath):
    try:
        with open(filePath, "w", encoding='utf-8') as f:
            f.write(browser.page_source)
    except:
        print("Could not download page!")

def readTikTok(intermediateFilePath, finalFilePath):
    with open(intermediateFilePath, 'r') as f:
        contents = f.read()
        soup = BS(contents, "html.parser")
        elements = soup.select('.css-1g95xhm-AVideoContainer.e19c29qe13')
        viewCount = soup.select('.css-ws4x78-StrongVideoCount.etrd4pu10')
        dates = soup.select('.css-dennn6-DivTimeTag.e19c29qe24')
        links = []

        for index, el in enumerate(elements):
            e = []
            l = el['href']
            e.append(l)

            img_tag = el.find('img') 
            if img_tag and 'alt' in img_tag.attrs: 
                alt_text = img_tag['alt']
                e.append(alt_text)
                
            if index < len(viewCount):
                view_text = viewCount[index].get_text(strip=True)
                e.append(view_text)
            else:
                e.append("No View Count Available")
            
            if index < len(dates):
                date_text = dates[index].get_text(strip=True)
                e.append(date_text)
            else:
                e.append("No Date Available")
            
            links.append(e)

        
        fileExists = os.path.isfile(finalFilePath)
        isEmpty = os.stat(finalFilePath).st_size == 0 if fileExists else True
        header = ['link', 'text', 'views', 'date']
        with open(finalFilePath, "a") as file:
            writer = csv.writer(file)
            if isEmpty:
                writer.writerow(header)
            for item in links:
                    writer.writerow(item)


def getTikTok(term, browser):
    if not os.path.isdir('./intermediate'):
        os.mkdir('./intermediate')

    if not os.path.isdir('./data'):
        os.mkdir('./data')

    if not os.path.isdir('./screenshots'):
        os.mkdir('./screenshots')
    intermediateFilePath = f'./intermediate/{term}_{datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")}.html'
    finalFilePath = f'./data/{term}_{datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")}.csv'

    browser.get(f'https://www.tiktok.com/search?q={term}')
    time.sleep(10)
    for i in range(0, lengthOfScroll):
        if i != 0:
            ActionChains(browser)\
                .scroll_by_amount(0, 900)\
                .perform()
        time.sleep(5)
        browser.save_screenshot(f'./screenshots/{term}_{datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")}.png')
        downloadPage(browser, intermediateFilePath)
        readTikTok(intermediateFilePath, finalFilePath)
    
    return finalFilePath

########################################
# Run unschooling queries
########################################
browser = startBrowser()

if login == False:
    for search in searchTerm:
        filePath = getTikTok(search, browser)

browser.quit()
