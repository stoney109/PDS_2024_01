import pandas as pd
from datetime import datetime, timedelta


def preprocess_birth(dataframe):
    """
    '출생연도' 데이터를 전처리하는 함수

    Parameters:
        dataframe (pd.DataFrame): 전처리할 데이터프레임

    Returns:
        pd.DataFrame: 전처리된 데이터프레임
    """
    # '(년생)'값 제거
    dataframe['출생연도'] = dataframe['출생연도'].str.replace(r'\(년생\)', '', regex=True)

    # 특수기호 제거 (e.g. '.', '_')
    dataframe['출생연도'] = dataframe['출생연도'].str.replace(r'[^0-9]', '', regex=True)

    # 두 자릿수 또는 한 자릿수 오류 처리
    def adjust_year_format(year):
        year = year.strip()  # 앞뒤 공백 제거
        if year.isdigit():  # 숫자인 경우
            if len(year) == 2:  # 두 자릿수라면 앞에 20을 붙임
                return '20' + year
            elif len(year) == 1:  # 한 자릿수라면
                if year in ['1', '2']:  # 1 또는 2라면 202를 붙임
                    return '202' + year
                else:  # 그 외의 숫자라면 201을 붙임
                    return '201' + year
        return year

    dataframe['출생연도'] = dataframe['출생연도'].apply(adjust_year_format)

    # 출생연도가 '60일미만'인 경우, 접수일 기준 2달 전 날짜로 업데이트
    for idx, row in dataframe.iterrows():
        if '60일미만' in row['출생연도']:
            # 접수일을 날짜 형식으로 변환
            registration_date = datetime.strptime(str(row['접수일']), '%Y%m%d')

            # 출생연도를 60일 전으로 계산하여 업데이트
            birth_date = registration_date - timedelta(days=60)
            dataframe.at[idx, '출생연도'] = birth_date.strftime('%Y.%m.%d')
        elif len(row['출생연도']) > 4:
            # 4자리 이상인 경우 앞의 4자리만 남김
            dataframe.at[idx, '출생연도'] = row['출생연도'][:4]

    # '20nn' 형태만 남아있으면 '20nn.01.01'으로 수정
    year_only_mask = dataframe['출생연도'].str.match(r'^20\d{2}$')
    dataframe.loc[year_only_mask, '출생연도'] = dataframe.loc[year_only_mask, '출생연도'] + '.01.01'

    # 출생연도에서 마지막 3글자를 제거 : 나이를 세는 데에 있어 year-month까지만 활용하기로 하여 date값을 삭제
    dataframe['출생연도'] = dataframe['출생연도'].str[:-3]

    return dataframe


def add_age_column(dataframe):
    """
    '나이' 컬럼을 '출생연도'와 '접수일'을 기준으로 계산하여 추가하는 함수

    Parameters:
        dataframe (pd.DataFrame): 나이를 계산할 데이터프레임

    Returns:
        pd.DataFrame: 나이가 추가된 데이터프레임
    """
    def calculate_age(row):
        try:
            # 출생연도를 datetime 객체로 변환
            birth_date = datetime.strptime(row['출생연도'], '%Y.%m')
            # 접수일을 datetime 객체로 변환
            registration_date = datetime.strptime(str(row['접수일']), '%Y%m%d')
            # 나이를 연 단위로 계산
            age = (registration_date - birth_date).days / 365.25  # 윤년 고려
            if age < 0:  # 음수 값 처리
                return 0  # 음수인 경우 0으로 처리 (총 117개의 입력 오류 데이터)
            return round(age, 1)  # 소수점 첫째 자리까지 반올림
        except Exception as e:
            return None  # 변환 실패 시 NaN 처리

    dataframe['나이'] = dataframe.apply(calculate_age, axis=1)
    return dataframe


# CSV 파일 경로
input_csv_file = 'preprocessing_csv_files/nonglim_base_preprocessing.csv'
output_csv_file = 'preprocessing_csv_files/nonglim_birth_preprocessing.csv'

# CSV 파일 읽기
data = pd.read_csv(input_csv_file)

# 출생연도 전처리 함수 수행
processed_data = preprocess_birth(data)

# 나이 컬럼 추가
processed_data = add_age_column(processed_data)

# 최종 데이터프레임을 CSV로 저장
processed_data.to_csv(output_csv_file, encoding='utf-8-sig', index=False)

# 처리된 요소 수 출력
num_elements = len(processed_data)
print(f'처리된 데이터의 수: {num_elements}개')