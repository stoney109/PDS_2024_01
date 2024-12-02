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

    # 출생연도가 '60일미만'인 경우, 접수일 기준 2달 전 날짜로 업데이트
    for idx, row in dataframe.iterrows():
        if '60일미만' in row['출생연도']:
            # 접수일을 날짜 형식으로 변환
            registration_date = datetime.strptime(str(row['접수일']), '%Y%m%d')

            # 출생연도를 60일 전으로 계산하여 업데이트
            birth_date = registration_date - timedelta(days=60)
            dataframe.at[idx, '출생연도'] = birth_date.strftime('%Y.%m.%d')

    # '20nn' 형태만 남아있으면 '20nn.01.01'으로 수정
    year_only_mask = dataframe['출생연도'].str.match(r'^20\d{2}$')
    dataframe.loc[year_only_mask, '출생연도'] = dataframe.loc[year_only_mask, '출생연도'] + '.01.01'

    # 출생연도에서 마지막 3글자를 제거 : 나이를 세는 데에 있어 year-month까지만 활용하기로 하여 date값을 삭제
    dataframe['출생연도'] = dataframe['출생연도'].str[:-3]

    return dataframe

# CSV 파일 경로
input_csv_file = '../preprocessing_csv_files/nonglim_base_preprocessing.csv'
output_csv_file = '../preprocessing_csv_files/nonglim_birth_preprocessing.csv'

# CSV 파일 읽기
data = pd.read_csv(input_csv_file)

# 출생연도 전처리 함수 수행
processed_data = preprocess_birth(data)

# 최종 데이터프레임을 CSV로 저장
processed_data.to_csv(output_csv_file, encoding='utf-8-sig', index=False)

# 처리된 요소 수 출력
num_elements = len(processed_data)
print(f'처리된 데이터의 수: {num_elements}개')
