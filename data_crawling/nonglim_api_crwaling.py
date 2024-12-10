import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# 상수 정의
MAX_RETRIES = 5  # 최대 재시도 횟수
TIMEOUT = 300  # 요청 타임아웃 시간 (초)
SLEEP_TIME = 1  # 요청 실패 시 재시도 전 대기 시간 (초)


def fetch_data(page_number):
    """
        각 페이지의 유기 동물 데이터를 API에서 가져와 처리

        Args:
            page_number (int): 가져올 페이지 번호

        Returns:
            list: 페이지에서 추출된 데이터 리스트
    """
    retries = 0

    while retries < MAX_RETRIES:
        try:
            # API 기본 정보
            service_key = '4KSeIIQIfZQtBMAivNP%2BlJMn4Q1vkCI3Q6dRaPwtCM6xprN45YhEEZYdQOUiWx%2BAaZ6PoEULHwO%2BHaMJwpH2zw%3D%3D'
            main_url = 'http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic?'
            begin_date = 'bgnde=20200101&'
            end_date = 'endde=20231116&'
            page_param  = f'pageNo={page_number}&'
            elem_param = 'numOfRows=1000&'
            service_url = f'serviceKey={service_key}'

            # HTTP 요청 헤더
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # API 요청
            response = requests.get(
                main_url + begin_date + end_date + page_param + elem_param + service_url,
                headers=headers,
                timeout=TIMEOUT
            )
            # HTTP 오류 확인
            response.raise_for_status()

            # HTML 파싱
            soup = BeautifulSoup(response.text, "lxml-xml")
            dog_information_area = soup.select('item')

            # 데이터 추출
            page_data = []

            #for 문을 돌며 필요한 데이터 수집
            for sample in dog_information_area:
                # 유기번호
                abandoned_id = sample.select_one('desertionNo').text
                # 국가동물정보보호시스템에 등록된 접수일 기준
                happen_date = sample.select_one('happenDt').text
                # 발견 장소
                happen_place = sample.select_one('happenPlace').text
                # 품종
                kind = sample.select_one('kindCd').text
                # 색상
                color = sample.select_one('colorCd').text
                # 나이
                age = sample.select_one('age').text
                # 체중
                weight = sample.select_one('weight').text
                # 유기 공고 시작일
                notice_start = sample.select_one('noticeSdt').text
                # 유기 공고 종료일
                notice_end = sample.select_one('noticeEdt').text
                # 이미지
                picture = sample.select_one('popfile').text
                # 보호상태(e.g. 보호중)
                process_state = sample.select_one('processState').text
                # 성별(M: 수컷, F:암컷, Q:미상)
                sex = sample.select_one('sexCd').text
                # 중성화여부 (Y: 예, N: 아니오, U: 미상)
                neutral = sample.select_one('neuterYn').text
                # 특징
                special = sample.select_one('specialMark').text
                # 보호소이름(e.g. 이기영수의과병원)
                care_center_name = sample.select_one('careNm').text
                # 보호장소(e.g. 충청남도 공주시 감영길 7 (반죽동))
                care_center_address = sample.select_one('careAddr').text

                page_data.append([abandoned_id, happen_date, happen_place, kind, color, age, weight, notice_start, notice_end,
                             picture, process_state, sex, neutral, special, care_center_name, care_center_address])

            return page_data

        except requests.exceptions.ConnectTimeout as timeout_err:
            print(f"타임아웃 발생 위치 : {timeout_err}")
            retries += 1
            time.sleep(SLEEP_TIME)  # 쉬는 시간 추가

        except requests.exceptions.RequestException as err:
            print(f"오류 발생 위치 : {err}")
            retries += 1
            time.sleep(SLEEP_TIME)  # 쉬는 시간 추가

    print(f"최대 재시도 횟수를 초과했습니다. 페이지 {page_number} 건너뜀.")
    return []


def fetch_all_pages(total_pages):
    """
        모든 페이지에서 데이터를 병렬로 처리 (시간 단축 목적)

        Args:
            total_pages (int): 가져올 페이지 총 개수.

        Returns:
            list: 모든 페이지에서 가져온 데이터를 합친 리스트.
    """
    all_data = []  # 데이터를 저장할 리스트

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_data, page) for page in range(1, total_pages + 1)]
        for future in as_completed(futures):
            all_data.extend(future.result())

    return all_data


if __name__ == "__main__":
    # 실행 시간 측정 시작
    start_time = time.time()

    try:
        # 총 340페이지 데이터를 가져옴, 2023년 11월 16일 기준 마지막 페이지 (339,615개의 데이터, 1페이지 당 1000개)
        # 약 17~20분 정도 소요됨 : 2024 11월 25일 기준 데이터 업데이트로 인해 개수가 과거와 달라짐 (222416개의 데이터)
        result_info_out = fetch_all_pages(340)

        # 데이터프레임 생성
        columns_names = ['ID', '접수일', '발견장소', '품종', '색상', '나이', '체중', '공고시작일', '공고종료일',
                         '사진', '상태', '성별', '중성화 여부', '특징', '보호소 이름', '보호장소']
        df = pd.DataFrame(result_info_out, columns=columns_names)

        # 필요한 컬럼만 선택
        selected_columns = ['접수일', '품종', '색상', '나이', '체중', '사진', '상태', '성별', '중성화 여부', '특징', '보호장소']
        df_selected = df[selected_columns]

        # 컬럼 이름 변경 (다른 크롤링 데이터 세트와 형태 통일)
        df_selected = df_selected.rename(columns={
            '품종': '견종',
            '나이': '출생연도',
            '사진': '썸네일',
            '상태': '입양여부'
        })

        # 최종 CSV 저장
        output_filename = '../resource/crawing_data/nonglim_crawling_20231116.csv'
        df_selected.to_csv(output_filename, encoding='utf-8-sig', index=False)

        print(f"크롤링 완료: 총 {len(result_info_out)}개 데이터를 수집했습니다.")

    except requests.exceptions.RequestException as e:
        print(f"에러 발생 : {e}")

    finally:
        # 실행 시간 측정 종료
        end_time = time.time()
        execution_time = end_time - start_time

        # 분과 초로 변환
        minutes, seconds = divmod(execution_time, 60)

        print(f"코드 실행 시간: {int(minutes)}분 {int(seconds)}초")