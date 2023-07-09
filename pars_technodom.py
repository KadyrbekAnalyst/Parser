import requests
from bs4 import BeautifulSoup as Bs
import fake_useragent


url = 'https://www.technodom.kz/search?recommended_by=instant_search&recommended_code=iphone&r46_search_query=iphone&r46_input_query=iphone'
# url_2 ='https://www.technodom.kz/p/smartfon-apple-iphone-11-128gb-black-mhdh3rma-228942?recommended_by=full_search&recommended_code=iphone'
ua = fake_useragent.UserAgent()

req = requests.get(url, headers={'user-agent':ua.random})
if req.status_code == 200:
    print('yes_connection')
src = req.text
soup = Bs(src, "lxml")
print(src)
# list_of_items = soup.find_all(class_='Typography Typography__Heading Typography__Heading_H1')
# print(list_of_items)
# for items in list_of_items:
#     print(items.get('href'))
    
# all_a = soup.find_all('a')
# for item in all_a:
#     item_text = item.text
#     item_url = item.get('href')
#     print(f'{item_text}:{item_url}')
    