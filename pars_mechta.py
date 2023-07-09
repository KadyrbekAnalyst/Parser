import requests
from bs4 import BeautifulSoup as Bs
import fake_useragent
from selenium import webdriver
import time

def data_get_selenium(url):
    driver = webdriver.Chrome()
    try:
        driver.get(url=url)
        time.sleep(7)
        with open('mechta_selenium.html','w',encoding='utf-8') as f:
            f.write(driver.page_source)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        
def data_for_uniq(url):
    driver = webdriver.Chrome()
    try:
        driver.get(url=url)
        time.sleep(5)
        with open('mechta_selenium_uniq.html','w',encoding='utf-8') as f:
            f.write(driver.page_source)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

def get_stop_flag(url):
    with open('mechta_selenium.html',encoding='utf-8') as f:
        src = f.read()
    soup = Bs(src,'lxml')
    flag = soup.find_all(class_ = 'q-mb-lg text-color3')
    if len(flag) > 0:
        return True
    else:
        return False
    
def read_local_html(html):
    urls = []
    with open(html,encoding='utf-8') as f:
        src = f.read()
    soup = Bs(src,'lxml')

    all_urls = soup.find_all('a')
    for items in all_urls:
        urls_text = items.get('href')
        if 'https://www.mechta.kz/product/' in str(urls_text):
            urls.append(urls_text)
    return urls

def data_get_from_requsets(html):
    with open(html,encoding='utf-8') as f:
        src = f.read()
    soup = Bs(src,'lxml')

    name = soup.find_all(class_='text-ts5')
    price = soup.find_all(class_='text-bold text-ts5 text-color1')
    return [name[0].text,price[0].text]

    
    
def get_all_info(product):
    all_info = []
    max_pages = 19
    for page in range(18,max_pages+1):
        url = f'https://www.mechta.kz/search/?q={product}&setcity=al&page={page}'
        data_get_selenium(url)
        if get_stop_flag(url):
            break
        else:
            urls = read_local_html('mechta_selenium.html')
            for links in urls:
                data_for_uniq(links)
                info = data_get_from_requsets('mechta_selenium_uniq.html')
                all_info.append({'links':links,'name':info[0],'price':info[1]})
                print(all_info)
 
get_all_info('iphone')
# a = get_stop_flag('https://www.mechta.kz/search/?q=iphone&setcity=al&page=19')
# print(a)       
# data_for_uniq('https://www.mechta.kz/product/televizor-samsung-led-ue55au7100uxce-uhd-smart/')
# info = data_get_from_requsets('mechta_selenium_uniq.html')
# data_get_selenium('https://www.mechta.kz/search/?q=iphone&setcity=al&page=19')
# a = read_local_html('mechta_selenium.html')
# for links in a:
#     data_get_from_requsets(links)
