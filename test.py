import requests
import time
import csv
import os
import json
from bs4 import BeautifulSoup
from datetime import datetime
import unicodedata

csv_file_path = 'csv/link_osn.csv'
parsed_urls_file = 'csv/parsed_urls.txt'  # File to store the parsed URLs

keywords = []
with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        keywords.append(row[0])

parsed_urls = set()  # Set to store the parsed URLs

# Load previously parsed URLs from the file
if os.path.exists(parsed_urls_file):
    with open(parsed_urls_file, 'r') as file:
        for line in file:
            parsed_urls.add(line.strip())

for keyword in keywords:
    url = f'https://krisha.kz{keyword}'

    # Skip already parsed URLs
    if url in parsed_urls:
        print(f"URL '{url}' has already been parsed. Skipping...")
        continue

    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")

    # name = soup.find(attrs={'class': "offer__advert-title"}).text.strip()
    name_element = soup.find('div', class_='offer__advert-title')
    name = name_element.text.strip() if name_element else ""
    # print(name)



    cam_list = soup.find_all(attrs={'class': "complex-parameters__container complex-parameters__container--infrastructure complex-parameters__container--has-expand"})
    cam = {cam.text.strip().replace('\n', '') for cam in cam_list} if cam_list else{}

    comp_list = soup.find_all(attrs={'class': "complex__sidebar-info-text"})
    comp = [comp.text.strip().replace('\n', '') for comp in comp_list] if comp_list else[]

    address = comp[2]
    developer = comp[3]
    
    try:
        floors_element = soup.find('dt', attrs={'data-name': 'count.of.floors'})
        floor_element = floors_element.find_next_sibling('dd')
        floors = floor_element.text.strip()
    except:
        floors = "--"

    try:
        aparts_element = soup.find('dt', attrs={'data-name': 'count.of.apartments'})
        apart_element = aparts_element.find_next_sibling('dd')
        apart = apart_element.text.strip()
    except:
        apart = "--"
    
    try:
        parking_element = soup.find('dt', attrs={'data-name': 'parking'})
        park_element = parking_element.find_next_sibling('dd')
        parking = park_element.text.strip()
    except:
        parking = "--"

    try:
        classes_element = soup.find('dt', attrs={'data-name': 'housingClass'})
        class_element = classes_element.find_next_sibling('dd')
        classes = class_element.text.strip()
    except:
        classes = "--"

    try:
        status_element = soup.find('div', attrs={'data-name': 'home.state'})
        stat_element = status_element.find('p')
        status = stat_element.text.strip()
    except:
        status = "--"

    try:
        deadline_element = soup.find('div', attrs={'data-name': 'deadline'})
        dead_element = deadline_element.find('p')
        deadline = dead_element.text.strip()
    except:
        deadline = "--"

    try:
        price_elem = soup.find(attrs={'class': "offer__price"})
        price = unicodedata.normalize("NFKD", price_elem.text).strip()
    except AttributeError:
        price = "--"

    video_surveillance_present = False

    for item in cam:
        if 'Видеонаблюдение' in item:
            video_surveillance_present = True
            break

    if video_surveillance_present:
        cam = 'YES'
    else:
        cam = '--'

    date = datetime.now().strftime('%d-%m-%Y')





    try:
        check = soup.find(attrs={'class': "reliability-block__text"}).text.strip()
    except AttributeError:
        check = "--"

    permission_list = soup.find_all(attrs={'class': "reliability-block__list"})
    all_permissions = {all_permissions.text.strip().replace('\n', '') for all_permissions in permission_list} if permission_list else{}

    if all_permissions == {}:
        all_permissions = check

    if all_permissions == 'Застройщик не предоставил разрешающих документов':
        yes_column = 'no'
        number_column = '--'
    elif all_permissions == 'Застройщик не предоставил разрешающих документов' or all_permissions == 'Нет разрешения на строительство':
        yes_column = 'no'
        number_column = '--'
    elif all_permissions == 'Застройщик не предоставил разрешающих документов' or all_permissions == 'Нет разрешения на привлечение средств дольщиков':
        yes_column = 'no'
        number_column = '--'
    elif all_permissions == 'Нет разрешения на строительство' and all_permissions == 'Нет разрешения на привлечение средств дольщиков':
        yes_column = 'no'
        number_column = '--'
    elif all_permissions == '--':
        yes_column = 'no info'
        number_column = '--'
    else :
        yes_column = 'yes'
        number_column = all_permissions


    gask = ''
    gask_elements = soup.find_all('div', attrs={'aria-describedby': 'tooltip'})  # Находим все элементы div с атрибутом aria-describedby равным "tooltip"
    gask_list = []  # Создаем пустой список для сохранения значений gask

    for gask_element in gask_elements:
        try:
            gask = gask_element.find('p').text.strip()  # Находим элемент p внутри текущего блока и получаем его текст
            gask_list.append(gask)  # Добавляем значение gask в список
            # print(gask_list)
        except:
            gask_list = '--'

    # print(gask_list)
    with open(f"csv/ads.csv", "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['name', 'price', 'status', 'deadline', 'address', 'developer', 'floors', 'apartments', 'cameras', 'gask','yes/no', 'number', 'link', 'date'])
        writer.writerow(
            (
                name,
                price,
                status,
                deadline,
                address,
                developer,
                floors,
                apart,
                cam,
                gask_list,
                yes_column,
                number_column,
                url,
                date
            )
        )

    # Add the parsed URL to the set
    parsed_urls.add(url)

    # Print the progress
    print(f"{url} processed")

# Save the parsed URLs to the file
with open(parsed_urls_file, 'w') as file:
    file.write('\n'.join(parsed_urls))

print("Parsing completed!")

