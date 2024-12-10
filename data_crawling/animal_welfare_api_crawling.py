from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

browser = webdriver.Chrome()
browser.get('http://openapi.seoul.go.kr:8088/5a4946746b363467353967464c596c/xml/TbAdpWaitAnimalView/1/1000/')
time.sleep(1)

html = browser.page_source
soup = BeautifulSoup(html, "html.parser")

dog_information_area = soup.select('row')
dog_information_area = list(set(dog_information_area))
print(len(dog_information_area))

trait_list = []
id_num = 1

for sample in dog_information_area:
    trait_elem = sample.select_one('INTRCN_CN')
    trait_tx = re.sub(r'<.*?>', '', trait_elem.get_text())
    trait = trait_tx.replace('\ufeff', '').replace('&nbsp;', '')
    name_elem = sample.select_one('NM')
    name = re.sub(r'<.*?>', '', name_elem.get_text())
    trait_list.append([id_num, name, trait])

    id_num += 1

    if len(trait_list) == 50:
        break

column_names = ['ID', '이름', '특징']
df = pd.DataFrame(trait_list, columns=column_names)
df.to_csv('seoul_ex.csv', encoding='utf-8-sig', index=False)

print(trait_list)

browser.quit()