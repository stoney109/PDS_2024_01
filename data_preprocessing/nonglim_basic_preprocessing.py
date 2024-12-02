import pandas as pd
import re


def preprocess_dataframe(dataframe):
    """
    데이터프레임의 주요 컬럼('견종', '체중', '보호장소', '특징') 데이터를 1차 전처리하는 함수

    Parameters:
        dataframe (pd.DataFrame): 전처리할 데이터프레임

    Returns:
        pd.DataFrame: 전처리된 데이터프레임
    """
    # '[개]'가 포함된 '견종' 열 데이터를 필터링
    dataframe = dataframe[dataframe['견종'].str.contains(r'\[개\]', na=False)].copy()

    # '견종' 열에서 '[개]' 문자열 제거
    dataframe['견종'] = dataframe['견종'].str.replace(r'\[개\] ', '', regex=True)

    # '체중' 열에서 '(Kg)' 문자열 제거
    dataframe['체중'] = dataframe['체중'].str.replace(r'\(Kg\)', '', regex=True)

    # '보호장소' 열에서 시군구 이름만 추출
    dataframe['보호장소'] = dataframe['보호장소'].str.extract(r'(\S+\s+\S+)')

    # '보호장소' 열에서 이중 공백을 단일 공백으로 변경
    dataframe['보호장소'] = dataframe['보호장소'].replace(['  '], ' ')

    # '특징' 열 데이터 전처리
    def clean_feature(text):
        """
        '특징' 컬럼에서 불필요한 요소를 제거하는 함수

        Parameters:
            text (str): 원본 텍스트 데이터

        Returns:
            str: 정제된 텍스트 데이터
        """
        if pd.notnull(text):
            # 대괄호([]) 사이의 값을 제거
            text = re.sub(r'\[.*?]', '', text)

            # '개체관리번호' 형식의 부분을 제거
            text = re.sub(r'개체관리번호 \d+(?:\s*-\s*|\b)', '', text)
            text = re.sub(r'\(개체관리번호 \d+\)|\(개체관리번호\d+\)', '', text)

            # '관리번호 :'와 관련된 패턴 제거
            text = re.sub(r'관리번호:\s*\d+(?:-\d+)?,?', '', text)

            # '00호(관리)', '00호(공고)' 형태의 문자열 제거
            text = re.sub(r'\d+호\((?:관리|공고)\),?', '', text)

            # 특정 형식(김해시-, 야생-, 등)을 제거
            text = re.sub(r'(김해시-\d+|김해-\d+|사상구-\d+|야생-\d+|[NKL]-\d+(?:-\d+)*),?', '', text)

            # '사상구-숫자,' 형태의 문자열 제거
            text = re.sub(r'사상구-\d+,? ', '', text)

            # '야생-숫자,' 형태의 문자열 제거
            text = re.sub(r'야생-\d+,? ', '', text)

            # 'N-숫자' 형태의 문자열 제거
            text = re.sub(r'[NKL]-\d+(?:-\d+)*,?', '', text)
            text = re.sub(r'-\(\d+\)', '', text)

            # '체중'과 관련된 문자열 제거
            text = re.sub(r'체중\d+kg|체중약\d+kg|체중\s*약\s*\d+\s*㎏|약체중\d+kg|체중갱신|체중추정|체중 갱신|체중갱', '', text)

            # 소괄호 제거
            text = text.replace('()', '')

            # '어미견', '모견', '자견', '남매', '번지'를 포함하지 않는 경우에만 '숫자-숫자' 형태의 문자열 제거
            # 명시해 놓은 일부 케이스에 대해서는 의미가 있는 정보를 포함하고 있음으로 제외
            if pd.notnull(text) and not any(keyword in text for keyword in ['어미', '모견', '자견', '새끼', '남매', '자매' '번지']):
                text = re.sub(r'\d+-\d+(?:,\d+-\d+)*', '', text)

            # 의미 없는 구문 및 특수 케이스 제거
            text = re.sub(r'mixed-breed dog\(믹스견\)|입양부탁드립니다|추후 사진수정하겠음|&#44501;움'
                          r'|★공고날짜 끝나고 입양문의 하세요★|구조날짜 9월22일', '', text) if pd.notnull(text) else text

            # 특징 컬럼의 데이터 형태 유사성을 위한 전처리
            # '.'과 '/'를 ','로 대체
            text = text.replace('.', ',').replace('/', ',')

            # 연속된 공백을 하나로 줄임
            text = re.sub(r'\s{2,}', ' ', text)

            # 콤마와 관련된 불필요한 공백 정리
            text = re.sub(r'\s*,\s*', ',', text)
            text = re.sub(r',+', ',', text)
            text = re.sub(r'^,', '', text)  # 제일 앞에 있는 ',' 제거
            text = re.sub(r'(.*),$', r'\1', text)  # 콤마가 글자에 붙어있어도 가장 뒤에 있다면 제거

            # 콤마 오른쪽에 ' ' 추가
            text = re.sub(r',', ', ', text)

        return text

    # '특징' 열 전처리 적용
    dataframe['특징'] = dataframe['특징'].apply(clean_feature)

    # '특징' 열 데이터의 앞뒤 공백 제거
    dataframe['특징'] = dataframe['특징'].str.strip()

    # '특징' 열에서 의미 없는 데이터 제거
    dataframe['특징'] = dataframe['특징'].replace(['번', '무', '없음', '-', '.', '..', '', ' '], '')

    return dataframe


# CSV 파일 경로 설정
input_csv_file = '../resource/crawing_data/nonglim_crawling_20231116.csv'
output_csv_file = 'preprocessing_csv_files/nonglim_base_preprocessing.csv'

# CSV 파일 읽기 (ID와 접수일 열의 데이터 타입을 object로 설정)
data = pd.read_csv(input_csv_file, dtype={'ID': 'object', '접수일': 'object'})

# 데이터 전처리 함수 호출
processed_data = preprocess_dataframe(data)

# 최종 데이터프레임을 CSV로 저장
processed_data.to_csv(output_csv_file, encoding='utf-8-sig', index=False)

# 처리된 요소 수 출력
num_elements = len(processed_data)
print(f'처리된 데이터의 수: {num_elements}개')
