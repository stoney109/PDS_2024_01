from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from urllib.parse import unquote, urljoin
import pandas as pd

browser = webdriver.Chrome()

number_link_list = [
    'https://cafe.naver.com/seoulanimalcare?iframe_url=/ArticleList.nhn%3Fsearch.clubid=29193247%26search.menuid=33%26search.boardtype=I%26search.totalCount=201%26search.cafeId=29193247%26search.page=' + str(i) for i in range(1, 19)
]


object_link_list = []
thumbnail_list = []
date_list = []
for number_link in number_link_list:
    browser.get(number_link)

    # WebDriverWait를 사용하여 페이지 로드 대기
    wait = WebDriverWait(browser, 10)
    wait.until(EC.title_contains('카페'))

    # iframe 내부로 전환
    browser.switch_to.frame(browser.find_element(By.NAME, "cafe_main"))

    # 페이지 소스 가져오기
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 게시글 링크 및 썸네일 선택자 수정
    object_area = soup.select('a.album-img')
    text_area = soup.select('dl')

    for sample in text_area:
        date = sample.select_one('span.date').text
        date_list.append(date)

    for sample in object_area:
        link = sample.get('href')
        object_link_list.append(link)

        thumbnail = sample.select_one('img').get('src')
        thumbnail_list.append(thumbnail)


title_list = []
text_list = []

for object in object_link_list:
    full_url = urljoin('https://cafe.naver.com/', object)
    modified_link = unquote(full_url, encoding='utf-8')

    print(modified_link)
    browser.get(modified_link)
    time.sleep(5)

    # iframe 내부로 전환
    browser.switch_to.frame(browser.find_element(By.NAME, "cafe_main"))

    # 페이지 소스 가져오기
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select_one('h3.title_text').text
    article_list = soup.select('p')
    title_list.append(title)
    article_text_list = [line.text for line in article_list]
    text_list.append(article_text_list)


# 여기에 추가: 수집된 데이터 출력 또는 저장
print(title_list,text_list)

# 브라우저 닫기
browser.quit()

final_result = []

for i in range(len(thumbnail_list)):
     date_i = date_list[i]
     thumbnail_i = thumbnail_list[i]
     title_i = title_list[i]
     text_i = text_list[i]
     final_result.append([date_i,thumbnail_i, title_i, text_i])

df = pd.DataFrame(final_result, columns=['date','썸네일','제목', '텍스트'])
df.to_csv('../resource/crawing_data/cafe_crawling_2024.csv', encoding='utf-8-sig')