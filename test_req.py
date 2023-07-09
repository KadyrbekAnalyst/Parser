import requests
from bs4 import BeautifulSoup as Bs
import fake_useragent
from selenium import webdriver
import time

url = 'https://www.technodom.kz/p/smartfon-apple-iphone-11-128gb-black-mhdh3rma-228942?recommended_by=full_search&recommended_code=Iphone'
ua = fake_useragent.UserAgent()
req = requests.get(url, headers={'user-agent':ua.random})
src = req.text
soup = Bs(src, "lxml")
a = soup.find_all(class_='Typography Typography__Heading Typography__Heading_H1')
print(a)

