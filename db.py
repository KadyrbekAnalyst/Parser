import requests
import time
import csv
import os
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs
import unicodedata
import hashlib
# import psycopg2


# database = "rwh_datalake"
# user = "rwh_analytics"
# password = "4HPzQt2HyU@"
# host = "172.30.227.205"
# port = "5439"

# # Подключение к PostgreSQL
# conn = psycopg2.connect(
#     host=host,
#     database=database,
#     user=user,
#     password=password,
#     port=port
# )

# cursor = conn.cursor()
# cursor.execute('''CREATE TABLE IF NOT EXISTS resumes(  
#             city TEXT, 
#             gender TEXT, 
#             name TEXT, 
#             specialization TEXT, 
#             age TEXT, 
#             salary TEXT, 
#             experience TEXT, 
#             experiences TEXT,
#             skills TEXT, 
#             link TEXT,
#             date DATE
#             );''')
# conn.commit()


# # Здесь путь к файлу CSV с ключевыми словами
# csv_file_path = 'csv/role.csv'

# Максимальное количество страниц для парсинга
max_pages = 100

# Чтение ключевых слов из файла CSV
# keywords = []
# with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         keywords.append(row[0])

# Перейти в папку с парсером
# os.chdir("C:/Users/User/OneDrive/Рабочий стол/try/pars")

# Загрузка списка уже спарсенных резюме
# parsed_resumes = []
# parsed_resumes_file = "parsed_resumes.txt"

# if os.path.exists(parsed_resumes_file):
#     with open(parsed_resumes_file, "r") as file:
#         parsed_resumes = file.read().splitlines()

# Базовый URL
base_url = 'https://hh.kz'

# Определение уникального имени файла
def get_unique_filename(keyword):
    # Замена запрещенных символов на подчеркивание
    keyword = keyword.replace(' ','_').replace('(','_').replace(')','').replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')

    # Составление уникального имени файла
    filename = f"resumes_{keyword}.csv"

    return filename

# Определение уникального идентификатора резюме
def get_unique_id(url):
    return hashlib.md5(url.encode()).hexdigest()

# Отправка запроса на каждую страницу для парсинга
# for i, keyword in enumerate(keywords):

# for page in range(0, 1):
url = f'https://hh.kz/search/resume?text=python&area=160&currency_code=KZT&ored_clusters=true&order_by=relevance&search_period=0&logic=normal&pos=full_text&exp_period=all_time&page=1'

# Обозначение user-agent и парсера (lxml)
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

req = requests.get(url, headers=headers)
src = req.text
soup = BeautifulSoup(src, "lxml")

# Ссылка на название вакансии
all_vacancy_hrefs=soup.find_all(class_="serp-item__title")
print(soup)

#         # Парсинг информации о резюме
# for item in all_vacancy_hrefs:
#     item_text = item.text
#     item_href = item.get("href")
#     print(item_href)
#             # Проверка новизны вакансии
#             if item_href in parsed_resumes:
#                 print(f'Резюме {item_href} уже спарсено. Пропуск...')
#                 continue

#             # Удаление ненужных символов из вывода данных
#             rep = [",", " ", "-", "<!-- -->", "\xa0"]
#             for item in rep:
#                 if item in item_text:
#                     item_text = item_text.replace(item, "_")

#             if item_href.startswith("/"):
#                 full_url = urljoin(base_url, item_href)
#             else:
#                 full_url = item_href

#             req = requests.get(full_url, headers=headers)
#             src = req.text
#             soup = BeautifulSoup(src, "lxml")

#             try:
#                 salary_elem = soup.find(attrs={'class': "resume-block__salary"})
#                 salary = unicodedata.normalize("NFKD", salary_elem.text).strip()
#             except AttributeError:
#                 salary = ""

#             skills_list = soup.find(attrs={'class': "bloko-tag-list"})
#             skills = [skill.text for skill in skills_list] if skills_list else []

#             try:
#                 specialization = soup.find(attrs={'class': "resume-block__specialization"}).text.strip()
#             except AttributeError:
#                 specialization = ""

#             try:
#                 experience = soup.find(attrs={'class': "resume-block__title-text resume-block__title-text_sub"}).text.strip()
#             except AttributeError:
#                 experience = ""

#             try:
#                 gender = soup.find(attrs={'data-qa': "resume-personal-gender"}).text.strip()
#             except AttributeError:
#                 gender = ""

#             try:
#                 city = soup.find(attrs={'data-qa': "resume-personal-address"}).text.strip()
#             except AttributeError:
#                 city = ""

#             try:
#                 experiences_elem = soup.find(attrs={'class': 'bloko-column bloko-column_xs-4 bloko-column_s-2 bloko-column_m-2 bloko-column_l-2'})
#                 experiences = unicodedata.normalize("NFKD", experiences_elem.text).strip()
#             except AttributeError:
#                 experiences = ""

#             try:
#                 age = soup.find(attrs={'data-qa': "resume-personal-age"}).text.strip()
#             except:
#                 age = ""

#             date = datetime.now().strftime('%Y-%m-%d')

#             # Проверка, является ли резюме уже спарсенным
#             if get_unique_id(item_href) in parsed_resumes:
#                 print(f'Резюме {item_href} уже спарсено. Пропуск...')
#                 continue

#             # Добавление резюме в список уже спарсенных
#             parsed_resumes.append(get_unique_id(item_href))

#             # Запись списка уже спарсенных резюме в файл
#             with open(parsed_resumes_file, "w") as file:
#                 file.write("\n".join(parsed_resumes))

#                 # Вставка данных в базу данных PostgreSQL
#                 cursor.execute(
#                     '''INSERT INTO resumes(city, gender, name, specialization, age, salary, experience, experiences, skills, link, date)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
#                     (city, gender, item_text, specialization, age, salary, experience, experiences, skills, item_href, date)
#                 )
#                 conn.commit()

#             # Пауза между запросами
#             time.sleep(1)

#         # Вывод прогресса
#         print(f"Страница {page + 1} из {max_pages} для {keyword} обработана")

# print("Парсинг завершен!")

# # Завершение транзакции и закрытие соединения с PostgreSQL
# cursor.close()
# conn.close()
