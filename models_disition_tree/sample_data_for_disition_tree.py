#샘플 데이터 (모델을 학습하기 위한 데이터)_apoted_data에서 추출
#disition tree를 사용하기 위해서는 x데이터를 수치형 데이터로 전처리
#disiton tree를 이용하실 때, final_00 컬럼을 사용하시면 됩니다
'''
x데이터 해석

견종 = 믹스 : 0, 믹스가 아닌 견종 : 1
나이 = 소수점 앞자리만 추출
체중 = 소수점에서 반올림
성별 = M : 0, F : 1, Q : 2
중성화여부 = Y : 0, N : 1, U : 2
'''

import pandas as pd
import numpy as np
import random

def preprocess_dog_data(file_path):
    #랜덤을 1만건의 데이터를 가져오기
    data = pd.read_csv(file_path)
    data = data.sample(frac=1, random_state=random.randint(1, 10000))
    selected_data = data.head(10000)

    # 전처리를 위해 원본 데이터 복사하기
    selected_columns = selected_data[['견종', '나이', '체중', '성별', '중성화 여부', '입양여부']].copy()

    #성별과 중성화 여부에 결측치가 있을 시 제외하고 가져오기
    selected_columns = selected_columns[selected_columns['성별'].notna()]
    selected_columns = selected_columns[selected_columns['중성화 여부'].notna()]

    # 견종 전처리
    selected_columns['견종'] = np.where(selected_columns['견종'] == '믹스', 0, 1)

    # 나이 전처리
    selected_columns['나이'] = selected_columns['나이'].apply(lambda x: int(str(x).split('.')[0]))

    # 체중 전처리
    selected_columns['체중'] = selected_columns['체중'].round().astype(int)

    # 성별 전처리
    selected_columns['성별'] = selected_columns['성별'].map({'M': 0, 'F': 1, 'Q': 2})

    # 중성화여부 전처리
    selected_columns['중성화 여부'] = selected_columns['중성화 여부'].map({'Y': 0, 'N': 1, 'U': 2})

    # 원본 데이터와의 비교와 확인의 간결함을 위해 카피한 데이터 앞에 final이름 추가
    selected_columns.rename(columns={
        '견종': 'final_견종',
        '나이': 'final_나이',
        '체중': 'final_체중',
        '성별': 'final_성별',
        '중성화 여부': 'final_중성화 여부',
        '입양여부': 'final_입양여부'
    }, inplace=True)

    processed_data = pd.concat([selected_data.reset_index(drop=True), selected_columns.reset_index(drop=True)], axis=1)

    return processed_data

file_path = '../resource/final_adopted_data.csv'  # Replace with your file path
processed_file_path = 'sample_data/sample_data_disition_tree.csv'  # Path to save processed data

processed_data = preprocess_dog_data(file_path)

#csv로 저장
processed_data.to_csv(processed_file_path, index=False)