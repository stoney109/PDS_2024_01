#농림 축산부 api 데이터 크롤링 코드

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

browser = webdriver.Chrome()
browser.get('https://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic?bgnde=20211201&endde=20211231&pageNo=1&numOfRows=1000&serviceKey=sTWMGBxG3%2FGmGlewy7%2B4bO9lwc%2Bb7SOZB1kxXN8k1kEtxNvp57tbyhj8U5VbxL5M9TlHQ56RFOpEDUBykU%2FQDA%3D%3D')
time.sleep(1)

html = browser.page_source
soup = BeautifulSoup(html, "html.parser")

dog_information_area = soup.select('item')

result_information = []
#더 필요한 특성이 있으면, 변수 추가하기
for sample in dog_information_area:
    abandoned_id = sample.select_one('desertionNo').text
    thumbnail = sample.select_one('filename').text
    #happen_date = sample.select_one('happenDt').text
    #happen_place = sample.select_one('happenPlace').text
    kind = sample.select_one('kindCd').text
    color = sample.select_one('colorCd').text
    age = sample.select_one('age').text
    weight = sample.select_one('weight').text
    notice_start = sample.select_one('noticeSdt').text
    notice_end = sample.select_one('noticeEdt').text
    #state = sample.select_one('processState').text
    sex = sample.select_one('sexCd').text
    neutral = sample.select_one('neuterYn').text
    trait = sample.select_one('specialMark').text
    care_place = sample.select_one('careAddr').text
    care_name = sample.select_one('careNm').text

    result_information.append([abandoned_id, thumbnail, kind, color, age, weight, notice_start,notice_end,sex,neutral,trait,care_place,care_name])

df = pd.DataFrame(result_information, columns=['ID','썸네일', '종', '색깔','나이','무게','공고 시작일','공고 마감일','성별','중성화수술','특징','보호장소','보호소 이름'])
print(result_information)

browser.quit()