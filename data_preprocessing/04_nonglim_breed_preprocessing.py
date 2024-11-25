import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time


def preprocess_breed(dataframe):
    """
    '견종' 데이터를 전처리하는 함수

    Parameters:
        dataframe (pd.DataFrame): 전처리할 데이터프레임

    Returns:
        pd.DataFrame: 전처리된 데이터프레임
    """
    # 특정 패턴 제거
    patterns_to_remove = ['들믹스로 보임', '1개월령', '파티컬러', '엄마가', '로 추정', '엄마는', '블랙탄', '로보임', '인듯', '추정', '종류', '작은', '유사']
    for pattern in patterns_to_remove:
        dataframe['견종'] = dataframe['견종'].str.replace(pattern, '', regex=True)

    # 숫자 제거
    dataframe['견종'] = dataframe['견종'].apply(lambda x: re.sub(r'\d', '', x) if pd.notna(x) else x)

    # 특수 기호 제거
    dataframe['견종'] = dataframe['견종'].apply(lambda x: re.sub(r'[^\w\s]', '', x) if pd.notna(x) else x)

    # 모든 공백 제거
    dataframe['견종'] = dataframe['견종'].replace({' ': ''}, regex=True)

    # '믹스' 앞에만 띄어쓰기 한 칸
    dataframe['견종'] = dataframe['견종'].replace({'믹스': ' 믹스 '}, regex=True)

    # 앞뒤 공백 제거
    dataframe['견종'] = dataframe['견종'].str.lstrip().str.rstrip()

    # 메인 견종 대체 딕셔너리 정의 (순서 중요)
    main_breed_replacements = {
        # 내용 수정
        '시고르자브|믹스 견|혼합|잡종|혼종|들개': '믹스', '진도견|진도개|백구|황구': '진도', '진도와리트리버의|진도리버': '진도리트리버', '촬스스파니엘|찰스스패니얼': '찰스스파니엘',
        'kromforhrlander': '크롬폴란데', 'kooikerhon': '쿠이커혼제', '도사견': '도사', '블랙리트리버': '라브라도리트리버',
        '벨지안말리노이즈|벨지안쉽도그|벨지안그로넨달': '벨지안셰퍼드독', '장모흰색' : '장모치와와',
        '미니핀': '미니어쳐핀셔', '스코틀랜드쉽독|셀티': '셔틀랜드쉽독', '삽살이': '삽살개', '잉글랜드쉽독': '올드잉글리쉬쉽독', '요키': '요크셔테리어',
        '소프트코티드휘튼테리어': '아이리쉬소프트코튼휘튼테리어', '블랙셰퍼트': '저먼셰퍼드독', '몰키': '말티즈요크셔테리어', '미들아시안오브자카': '센트럴아시안오브차카',
        '브리똥': '브리타니스파니엘', '그레이트마운틴': '버니즈마운틴독', '바이마라너': '와이마라너',
        '켈피': '오스트레일리안켈피', '잉글리쉬불독': '프렌치불독', '포메허스키': '포메라니안허스키', '래빗닥스훈드': '래빗닥스훈트', '풍산개': '풍산견',

        # 오타 수정
        '발발이': '발바리', '포인트': '포인터', '허스키로': '허스키', '말티즈로': '말티즈', '포메라니언': '포메라니안', '최와와': '치와와', '슈나우저|쉬나우저': '슈나우져',
        '슈나이져진도': '슈나우져진도', '저먼스패니얼': '저먼스파니엘', '사모에드': '사모예드', '푸들과': '푸들', '사모예드와차우차우': '사모예드차우차우', '세퍼드': '셰퍼드',
        '세테': '세터', '리트리버와웰시코기': '리트리버웰시코기', '허스키와웰시코기': '허스키웰시코기', '보도콜리': '보더콜리', '시바견': '시바',

        # 믹스 처리
        '말티 믹스': '말티즈 믹스', '말티푸 믹스들 믹스 로보임|말티즈푸들말티푸|맡티푸|푸들말티즈': '말티푸 믹스', '골든두들': '골든두들 믹스',
        '롯트와일러 믹스': '로트와일러 믹스', '세퍼트 믹스|셰퍼트 믹스': '셰퍼드 믹스', '테리어종 믹스': '테리어 믹스', '시츄말티 믹스|말티츄': '말티츄 믹스',
        '폼치포메치와와': '포메라니안치와와 믹스', '포메 믹스': '포메라니안 믹스', '코카 믹스': '코카스파니엘 믹스', '비숑 믹스': '비숑프리제 믹스',
        '풍산 믹스': '풍산견 믹스', '푸숑': '푸숑 믹스', '웰시리트리버 믹스': '웰시코기리트리버 믹스', '슈나 믹스': '슈나우져 믹스',
        '폼피츠포메스피츠|포메라니안스피츠폼피츠|포메스피츠|폼피스': '폼피츠 믹스', '라브라도 믹스': '라브라도리트리버 믹스', '삽살 믹스': '삽살개 믹스',
        '그레이드피레니즈 믹스': '그레이트피레니즈 믹스', '보스턴프렌치 믹스': '프렌치불독보스턴테리어 믹스', '웰시 믹스': '웰시코기 믹스'

    }
    dataframe['견종'] = dataframe['견종'].replace(main_breed_replacements, regex=True)

    # '알수없음' 추가 (추후 '믹스' 편입 여부 검토 가능)
    dataframe['견종'] = dataframe['견종'].replace({'품종구분불가|품종추정|호피 믹스|유기견|사냥견|사냥개|호피견|품종|기타|미상|댕견': '알수없음'}, regex=True)

    # 전체 일치 시에만 변환 딕셔너리 정의
    exact_match_replacements = {
        '^믹$': '믹스',
        '^엄$': '알수없음',
        '^포메$': '포메라니안',
        '^요크 믹스$': '요크셔테리어 믹스',
        '^닥스$': '닥스훈트',
        '^라브라도$': '라브라도리트리버',
        '^차우 믹스$': '차우차우 믹스',
        '^피레니즈 믹스$': '그레이트피레니즈 믹스',
        '^스프링거스파니엘$': '잉글리쉬스프링거스파니엘'
    }
    dataframe['견종'] = dataframe['견종'].replace(exact_match_replacements, regex=True)

    # 모든 공백 제거
    dataframe['견종'] = dataframe['견종'].replace({' ': ''}, regex=True)

    # '믹스' 앞에만 띄어쓰기 한 칸
    dataframe['견종'] = dataframe['견종'].replace({'믹스': ' 믹스 '}, regex=True)

    # 믹스 형태 통일 딕셔너리 정의
    mix_form_replacements = {
        '포인터세터 믹스|^포인터세터$': '세터포인터 믹스', '말티푸 믹스|^말티즈푸들$|말티푸': '말티즈푸들 믹스',
        '믹스 골든리트리버': '골든리트리버 믹스', '믹스 말티즈': '말티즈 믹스', '포메라니안치와와 믹스|^치와와포메라니안$': '치와와포메라니안 믹스',
        '시츄말티즈 믹스|말티츄 믹스|^말티즈시츄$': '말티즈시츄 믹스', '진도리트리버 믹스|^진도리트리버$': '리트리버진도 믹스',
        '웰시코기리트리버 믹스': '리트리버웰시코기 믹스', '포메라니안스피츠|폼피츠 믹스|포메스피츠|폼피츠': '스피츠포메라니안 믹스',
        '프렌치불독보스턴테리어 믹스': '보스턴테리어프렌치불독 믹스', '슈나우져말티즈 믹스': '말티즈슈나우져 믹스',
        '골든두들 믹스': '골든리트리버푸들 믹스', '허스키웰시코기 믹스': '웰시코기허스키 믹스', '푸숑 믹스': '비숑프리제푸들 믹스',
        '늑대 믹스': '울프독', '올드프렌치불독': '프렌치불독'
    }
    dataframe['견종'] = dataframe['견종'].replace(mix_form_replacements, regex=True)

    # 앞뒤 공백 제거
    dataframe['견종'] = dataframe['견종'].str.lstrip().str.rstrip()

    return dataframe


def fetch_dog_breed_from_api():
    """
    API를 통해 견종 데이터를 수집하는 함수

    Returns:
        pd.DataFrame: 수집된 견종 데이터프레임
    """
    result_information = []
    start_time = time.time()

    try:
        main_url = 'http://apis.data.go.kr/1543061/abandonmentPublicSrvc/kind?up_kind_cd=417000&serviceKey='
        service_key = 'sTWMGBxG3%2FGmGlewy7%2B4bO9lwc%2Bb7SOZB1kxXN8k1kEtxNvp57tbyhj8U5VbxL5M9TlHQ56RFOpEDUBykU%2FQDA%3D%3D'

        response = requests.get(main_url + service_key)

        soup = BeautifulSoup(response.text, "lxml-xml")

        dog_information_area = soup.select('item')

        for sample in dog_information_area:
            dog_name = sample.select_one('KNm').text
            result_information.append([dog_name])

        additional_breeds = ['알수없음', '리트리버', '웰시코기', '장모치와와', '스카이테리어', '세터', '하운드', '킹찰스스파니엘', '허스키', '저먼스파니엘', '캉갈',
                             '아펜핀셔', '딩고',  '러프콜리', '불개', '노르웨이언엘크하운드', '블루틱쿤하운드', '테리어', '쿠이커혼제', '크롬폴란데', '발바리',
                             '미니어쳐슈나우져', '보더테리어', '스키퍼키', '아메리칸브리타니', '코몬도르', '카라카찬독', '아이리쉬테리어', '티베탄테리어', '티베탄스파니엘',
                             '닥스훈트', '와이어폭스테리어', '스무스폭스테리어', '말티푸', '말티츄', '폼피츠', '라이카', '포인터', '골든두들', '푸들', '푸숑'
                            ]

        for breed in additional_breeds:
            result_information.append([breed])

    finally:
        end_time = time.time()
        execution_time = end_time - start_time

        # 분과 초로 변환
        minutes, seconds = divmod(execution_time, 60)

        print(f'API 데이터 수집 완료: {len(result_information)}개 견종 수집')
        print(f'수행 시간: {int(minutes)}분 {int(seconds)}초')

        df = pd.DataFrame(result_information, columns=['견종'])

        # 데이터 형태 통일을 위한 이름 변경
        df['견종'] = df['견종'].replace({'믹스견': '믹스', '진도견': '진도', '래빗 닥스훈드': '래빗닥스훈트'}, regex=True)

        # 소괄호 및 그 안의 문자열 제거
        df['견종'] = df['견종'].replace(r'\(.*?\)', '', regex=True)

        # '견종' 컬럼에서 공백 제거
        df['견종'] = df['견종'].replace({' ': ''}, regex=True)

        # '믹스' 앞에만 띄어쓰기 한 칸
        df['견종'] = df['견종'].replace({'믹스': ''}, regex=True)
        df['견종'] = df['견종'].replace({'': '믹스'}, regex=True)
        df['견종'] = df['견종'].replace({'기타': '알수없음'}, regex=True)

        # 앞뒤 공백 제거
        df['견종'] = df['견종'].str.lstrip().str.rstrip()

        # 중복 행 제거
        df = df.drop_duplicates()

        # 가나다 순으로 정렬
        df = df.sort_values(by='견종', key=lambda x: x.str.len(), ascending=False)

        # '믹스'를 가장 위로 옮기기
        mix_index = df[df['견종'] == '믹스'].index
        df = pd.concat([df.loc[mix_index], df.drop(mix_index)])

    return df


def separate_detail_breed(combination_data, breed_file):
    """
    견종 데이터를 처리하고, 각 조합에서 강아지 종을 분리하여 새 컬럼 '세부 견종'을 추가 생성

    Args:
        combination_data (pd.DataFrame): 견종 조합 데이터프레임
        breed_file (str): 견종 데이터 파일 경로 (CSV 파일 경로)

    Returns:
        pd.DataFrame: 처리 및 컬럼 순서가 재배치된 데이터프레임
    """
    # 견종 데이터 읽기
    breed_data = pd.read_csv(breed_file)
    breed_list = breed_data['견종'].tolist()

    # '견종' 데이터를 리스트로 변환
    breed_combinations = combination_data['견종'].tolist()

    # 각 조합을 분리하여 리스트에 추가
    detailed_breed_list = []
    for combination in breed_combinations:
        extracted_breeds = []
        if pd.notna(combination):  # NaN이 아닌 경우에만 처리
            # breed_list에 있는 견종으로 분리
            for breed in breed_list:
                if pd.notna(breed) and breed in combination:
                    extracted_breeds.append(breed)
            detailed_breed_list.append(extracted_breeds)
        else:
            detailed_breed_list.append([])  # NaN인 경우 빈 리스트 추가

    # '세부견종' 컬럼 추가 및 리스트를 문자열로 변환
    combination_data['세부견종'] = detailed_breed_list
    combination_data['세부견종'] = combination_data['세부견종'].apply(lambda x: ', '.join(map(str, x)))

    # 컬럼 순서
    column_order = [
        '접수일', '견종', '세부견종', '색상', '출생연도', '체중', '썸네일', '입양여부', '성별', '중성화 여부', '특징', '보호장소'
    ]

    # 컬럼 순서 재배치
    combination_data = combination_data[column_order]

    def preprocess_detail_breed(dataframe):
        """
        견종 데이터프레임에서 '세부견종'과 '견종'을 전처리하는 함수

        Parameters:
            dataframe (pd.DataFrame): 전처리할 데이터프레임

        Returns:
            pd.DataFrame: 전처리된 데이터프레임
        """
        # '세부견종' 컬럼에 '믹스'가 있는지 확인하고 처리
        # dataframe['견종'] = dataframe['세부견종'].apply(lambda x: '믹스' if pd.notna(x) and '믹스' in x else '')

        # '세부견종'에 '믹스'가 있는 경우에 '견종'에 '믹스' 입력
        dataframe.loc[dataframe['세부견종'].str.contains('믹스', na=False), '견종'] = '믹스'

        # '세부견종'에 있는 '믹스' 제거
        dataframe['세부견종'] = dataframe['세부견종'].str.replace('믹스, ', '', regex=False)

        # '견종' 컬럼이 '믹스'가 아닌 경우, '세부견종'에서 가장 긴 문자열만 남기기
        non_mix_mask = (dataframe['견종'] != '믹스')
        dataframe.loc[non_mix_mask, '세부견종'] = dataframe.loc[non_mix_mask, '세부견종'].apply(
            lambda x: max(x.split(', '), key=len) if pd.notna(x) else x
        )

        # '세부견종'에서 가장 뒤에 있는 콤마(,) 제거
        dataframe['세부견종'] = dataframe['세부견종'].str.rstrip(',')

        # 일부 '믹스'인 경우에 대한 처리 (eg. 보더콜리 믹스 >> 믹스 / 보더콜리)
        breed_replacements = {
            '^핏불테리어, 테리어$': '핏불테리어',
            '보더콜리, 콜리': '보더콜리',
            '라브라도리트리버, 리트리버': '라브라도리트리버',
            '프렌치불독, 불독': '프렌치불독',
            '보스턴테리어, 프렌치불독, 테리어, 불독': '보스턴테리어, 프렌치불독',
            '노퍽테리어, 테리어': '노퍽테리어',
            '아메리칸핏불테리어, 핏불테리어, 테리어': '아메리칸핏불테리어',
            '골든리트리버, 리트리버': '골든리트리버',
            '장모치와와, 치와와': '장모치와와',
            '골든리트리버, 리트리버, 푸들': '골든리트리버, 푸들',
            '시베리안허스키, 허스키': '시베리안허스키',
            '페터데일테리어, 테리어': '페터데일테리어',
            '요크셔테리어, 테리어, 말티즈': '요크셔테리어, 말티즈',
            '웰시코기카디건, 웰시코기': '웰시코기카디건',
            '케언테리어, 테리어': '케언테리어',
            '그레이하운드, 하운드': '그레이하운드',
            '잭러셀테리어, 테리어': '잭러셀테리어',
            '요크셔테리어, 테리어': '요크셔테리어'
        }
        dataframe['세부견종'] = dataframe['세부견종'].replace(breed_replacements, regex=True)

        # '견종' 컬럼이 비어 있는 경우, '세부견종'의 내용을 복사
        dataframe.loc[dataframe['견종'] == '', '견종'] = dataframe['세부견종']

        return dataframe

    # 함수 호출
    combination_data = preprocess_detail_breed(combination_data)

    return combination_data


# CSV 파일 경로
input_csv_file = 'preprocessing_csv_files/nonglim_color_preprocessing.csv'
output_csv_file = 'preprocessing_csv_files/nonglim_breed_preprocessing.csv'
breed_csv_file = '../resource/crawing_data/breed.csv'

# CSV 파일 읽기
data = pd.read_csv(input_csv_file)

# 견종 전처리 함수 수행
processed_data = preprocess_breed(data)

# # 견종 API 데이터 수집 수행
# api_breed_data = fetch_dog_breed_from_api()
#
# # 견종 API 데이터를 CSV로 저장
# api_breed_data.to_csv(breed_csv_file, encoding='utf-8-sig', index=False)

# 세부견종 분리 및 전처리 함수 수행
detail_processed_data = separate_detail_breed(processed_data, breed_csv_file)

# 최종 데이터프레임을 CSV로 저장
detail_processed_data.to_csv(output_csv_file, encoding='utf-8-sig', index=False)

# 처리된 요소 수 출력
num_elements = len(processed_data)
print(f'처리된 데이터의 수: {num_elements}개')