from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import pandas as pd

# Selenium을 사용하여 Chrome 브라우저를 열고 API URL로 이동
browser = webdriver.Chrome()
browser.get('http://openapi.seoul.go.kr:8088/5a4946746b363467353967464c596c/xml/TbAdpWaitAnimalView/1/1000/')

# 특정 태그가 로드될 때까지 대기
wait = WebDriverWait(browser, 20)
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'row')))  # 'row' 태그가 로드될 때까지 대기

# 페이지 소스를 가져와 BeautifulSoup 객체로 파싱
html = browser.page_source
soup = BeautifulSoup(html, "html.parser")

# API에서 제공하는 동물 정보를 포함한 'row' 태그를 선택
dog_information_area = soup.select('row')  # 'row' 태그를 선택
dog_information_area = list(set(dog_information_area))  # 중복된 데이터 제거

# 동물 정보를 저장할 리스트 및 ID 초기화
trait_list = []

# 가져온 DOG 정보에서 이름과 특징을 추출하여 trait_list에 저장
for sample in dog_information_area:
    # 동물의 특징(INTRCN_CN)을 가져옴
    trait_elem = sample.select_one('INTRCN_CN')
    trait_tx = re.sub(r'<.*?>', '', trait_elem.get_text())  # HTML 태그 제거
    trait = trait_tx.replace('\ufeff', '').replace('&nbsp;', '')  # 불필요한 문자를 제거

    # 동물의 이름(NM)을 가져옴
    name_elem = sample.select_one('NM')
    name = re.sub(r'<.*?>', '', name_elem.get_text())  # HTML 태그 제거

    #동물의 견종(BREEDS)을 가져옴
    species_elem = sample.select_one('BREEDS')
    species = re.sub(r'<.*?>', '', species_elem.get_text())

    #동물의 나이(AGE)를 가져옴
    age_elem = sample.select_one('AGE')
    age = re.sub(r'<.*?>', '', age_elem.get_text())

    # 동물의 입소날짜(ENTRNC_DATE)를 가져옴
    enter_data_elem = sample.select_one('ENTRNC_DATE')
    enter_data = re.sub(r'<.*?>', '', enter_data_elem.get_text())

    # 동물의 체중(BDWGH)를 가져옴
    bdwgh_elem = sample.select_one('BDWGH')
    bdwgh = re.sub(r'<.*?>', '', bdwgh_elem.get_text())

    # 동물의 소개동영상(INTRCN_MVP_URL)을 가져옴
    image_elem = sample.select_one('INTRCN_MVP_URL')
    image = re.sub(r'<.*?>', '', image_elem.get_text())

    #동물의 입양상태(ADP_STTUS)를 가져옴
    adoption_status_elem = sample.select_one('ADP_STTUS')
    adoption_status = re.sub(r'<.*?>', '', adoption_status_elem.get_text())

    # 동물의 성별(SEXDSTN)을 가져옴
    sex_elem = sample.select_one('INTRCN_MVP_URL')
    sex = re.sub(r'<.*?>', '', sex_elem.get_text())

    # ID, 이름, 특징 데이터를 trait_list에 추가
    trait_list.append([name, species, age, enter_data, bdwgh, image, adoption_status, sex, trait])

    # 50개의 데이터만 가져오도록 제한(사전에 먼저 데이터의 양 체크필요)
    if len(trait_list) == 50:
        break

# 데이터를 Pandas 데이터프레임으로 변환
column_names = ['이름','견종','나이','들어온 날짜','체중','소개동영상','입양상태','성별','특징']
df = pd.DataFrame(trait_list, columns=column_names)

# 데이터프레임을 CSV 파일로 저장 (UTF-8-SIG 인코딩 사용)
df.to_csv('../resource/crawling_data/seoul_crawling_2024.csv', encoding='utf-8-sig', index=False)  # 인덱스를 제외하고 저장

# 브라우저 닫기
browser.quit()