from bs4 import BeautifulSoup
from selenium import webdriver
import time

search = input('Search: ')
driver_location = "C:/Users/Nabin/Downloads/chromedriver/chromedriver.exe"
driver = webdriver.Chrome(driver_location)
driver.get("https://www.google.com/search?q={}".format('+'.join(search.split())))

time.sleep(1)
depth = 0
collected_links = dict()  # to store the number of times a particular website is encountered
# collected_links[link] = (first page link is encountered at, no of times it's encountered)
while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for y in soup.findAll("div", class_="g"):
        x = y.find("a")
        link = x.get("href")
        if not link:
            # if link == None
            continue
        mark = False
        if "https://" in link: mark = 8
        elif "http://" in link: mark = 7
        if not mark:
            # if the link doesn't start from https or http
            # then it's probably something else xD
            continue
        link = link[mark:]
        if '/' in link:
            link = link[:link.find('/')]
        if link in collected_links:
            firstpage, ntimes = collected_links[link]
            collected_links[link] = (firstpage, ntimes + 1)
        else:
            collected_links[link] = (depth, 1)
    new = '//*[@id="pnnext"]'  #XPath for the 'next page' button on google results page
    depth += 1
    try:
        driver.find_element_by_xpath(new).click()
    except:
        # google didn't show more results after this page
        print('over at depth:', depth)
        break
driver.close()

collected_links_list = [(link, tup) for link, tup in collected_links.items()]
collected_links_list.sort(key=lambda x: x[1][1], reverse=True)
collected_links_list.sort(key=lambda x: x[1][0])

with open('collected_links.txt', 'w') as file:
    for link, tup in collected_links_list:
        file.write(link + ' ' + str(tup[0] + 1) + ' ' + str(tup[1]) + ' ' + '\n')



