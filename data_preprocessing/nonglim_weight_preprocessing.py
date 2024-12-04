import pandas as pd


def preprocess_weight(dataframe):
    """
    '체중' 데이터를 전처리하는 함수

    Parameters:
        dataframe (pd.DataFrame): 전처리할 데이터프레임

    Returns:
        pd.DataFrame: '체중' 컬럼이 전처리된 데이터프레임
    """
    # 모든 공백 제거
    dataframe['체중'] = dataframe['체중'].replace({' ': ''}, regex=True)

    # 잘못된 데이터 수정 (말티즈임을 확인 -> 말티즈 평균 체중 정도인 3kg으로 변경)
    dataframe['체중'] = dataframe['체중'].replace({'670225': '3'}, regex=True)

    # '체중' 컬럼을 숫자형으로 변환
    dataframe['체중'] = pd.to_numeric(dataframe['체중'], errors='coerce')  # 변환 실패 시 NaN 처리

    # NaN 값이 있는 행 제거 (약 431개 추정)
    # NaN 제거 전 총 데이터 수: 243012개 -> 242581개
    dataframe = dataframe.dropna(subset=['체중'])

    # 100 이상인 체중 값을 kg 단위로 변환 (kg과 g 단위 통일)
    dataframe.loc[dataframe['체중'] >= 100, '체중'] /= 100

    return dataframe


# 체중 범위별 개수를 출력하는 함수 : 데이터 확인 및 오류 데이터 확인 용도
def print_weight_ranges(dataframe):
    ranges = [
        ("0.01 미만", dataframe[dataframe['체중'] < 0.01].shape[0]),    # 간혹 신생아 강아지들의 몸무게가 해당 범위에 포함됨
        ("0.1 미만", dataframe[dataframe['체중'] < 0.1].shape[0]),
        ("0.5 미만", dataframe[dataframe['체중'] < 0.5].shape[0]),
        ("1 미만", dataframe[dataframe['체중'] < 1].shape[0]),
        ("1 ~ 5 미만", dataframe[(dataframe['체중'] >= 1) & (dataframe['체중'] < 5)].shape[0]),
        ("5 ~ 10 미만", dataframe[(dataframe['체중'] >= 5) & (dataframe['체중'] < 10)].shape[0]),
        ("10 ~ 20 미만", dataframe[(dataframe['체중'] >= 10) & (dataframe['체중'] < 20)].shape[0]),
        ("20 이상", dataframe[dataframe['체중'] >= 20].shape[0]),
        ("30 이상", dataframe[dataframe['체중'] >= 30].shape[0]),
        ("50 이상", dataframe[dataframe['체중'] >= 50].shape[0])
    ]

    print("◆ 체중 범위별 마리 수 ◆")
    for label, count in ranges:
        print(f"{label}: {count}마리")


# CSV 파일 경로
input_csv_file = 'preprocessing_csv_files/nonglim_feature_preprocessing.csv'
output_csv_file = 'preprocessing_csv_files/nonglim_weight_preprocessing.csv'

# CSV 파일 읽기
data = pd.read_csv(input_csv_file)

# 체중 전처리 함수 수행
processed_data = preprocess_weight(data)

# 체중 범위별 개수 출력
# print_weight_ranges(processed_data)

# 최종 데이터프레임을 CSV로 저장
processed_data.to_csv(output_csv_file, encoding='utf-8-sig', index=False)

# 처리된 요소 수 출력
num_elements = len(processed_data)
print(f'처리된 데이터의 수: {num_elements}개')