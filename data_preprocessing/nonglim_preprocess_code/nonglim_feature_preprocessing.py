import pandas as pd
import re


def preprocess_feature(dataframe):
    """
    '특징' 데이터를 전처리하는 함수

    Parameters:
        dataframe (pd.DataFrame): 전처리할 데이터프레임

    Returns:
        pd.DataFrame: '특징' 컬럼이 전처리된 데이터프레임
    """
    def clean_text(text):
        """
        '특징' 컬럼의 개별 텍스트를 전처리하는 함수
        : 특징 컬럼의 다양항 휴먼에러와 변수가 많아 일부 경우에 대해서만 전처리 함

        Parameters:
            text (str): 원본 텍스트

        Returns:
            str: 전처리된 텍스트
        """
        # nan 값 체크
        if pd.isna(text):
            return text

        # 정규 표현식을 사용하여 제거할 패턴 찾기
        age_patterns = r'\d+~\d|\d+살|\d+주|추정|\d+개월|\d+개월령|\d+일령|생후|\d+년|\d+월생|\d+일|\d+세|입소 시|입소일 기준|개월|살|년|이상|된 강아지|미만|이하|정도|발견상태|발견당시|노견|령|보임'
        degree_patterns = r'얕은|엷은|짙은|양호|연|옅|은'
        symbol_patterns = r'[()?~&*+]'

        # '특징' 컬럼 값에서 대체 단어를 적용
        text = re.sub(age_patterns, '', text)
        text = re.sub(degree_patterns, '', text)
        text = re.sub(symbol_patterns, '', text)

        # 연속된 공백 하나로 변경
        text = re.sub(r'\s{2,}', ' ', text)

        # 콤마 앞뒤 공백 정리 및 중복된 콤마 제거
        text = re.sub(r'\s*,\s*', ',', text)
        text = re.sub(r',+', ',', text)

        # 콤마 위치 정리
        text = re.sub(r'^,', '', text)  # 제일 앞의 ',' 제거
        text = re.sub(r'(.*),$', r'\1', text)  # 마지막 ',' 제거

        # 콤마 뒤 공백 추가
        text = re.sub(r',', ', ', text)

        return text.strip()

    # '특징' 컬럼에 전처리 적용
    dataframe['특징'] = dataframe['특징'].apply(clean_text)

    return dataframe


# CSV 파일 경로
input_csv_file = '../preprocessing_csv_files/nonglim_breed_preprocessing.csv'
output_csv_file = '../preprocessing_csv_files/nonglim_feature_preprocessing.csv'

# CSV 파일 읽기
data = pd.read_csv(input_csv_file)

# 특징 전처리 함수 수행
processed_data = preprocess_feature(data)

# 최종 데이터프레임을 CSV로 저장
processed_data.to_csv(output_csv_file, encoding='utf-8-sig', index=False)

# 처리된 요소 수 출력
num_elements = len(processed_data)
print(f'처리된 데이터의 수: {num_elements}개')