#다른 방법의 전처리 방식
#모델의 성능을 테스트하기 위한 test_data를 전처리 하는 코드입니다
#disition tree를 사용하기 위해서는 x데이터를 수치형 데이터로 전처리
#disiton tree를 이용하실 때, final_00 컬럼을 사용하시면 됩니다
'''
x데이터 해석

견종 = 믹스 : 0, 믹스가 아닌 견종 : 1
나이 = 소수점 첫재짜리까지
체중 = 소수점 첫째짜리까지
(미상은 제외하고 추출)
성별 = M : 0, F : 1
중성화여부 = Y : 0, N : 1
'''

import pandas as pd
import numpy as np

def preprocess_dog_data(file_path):
    data = pd.read_csv(file_path)

    # 성별이 Q 또는 중성화 여부가 U인 데이터 제외
    filtered_data = data[(data['성별'] != 'Q') & (data['중성화 여부'] != 'U')]

    # 랜덤으로 10,000건의 데이터 가져오기
    sampled_data = filtered_data.sample(n=10000, random_state=42)

    # 전처리를 위해 필요한 컬럼만 추출
    selected_columns = sampled_data[['견종', '나이', '체중', '성별', '중성화 여부', '입양여부']].copy()

    # 견종 전처리
    selected_columns['견종'] = np.where(selected_columns['견종'] == '믹스', 0, 1)

    # 나이 전처리 (소수점 첫째 자리까지만 유지)
    selected_columns['나이'] = selected_columns['나이'].round(1)

    # 체중 전처리 (소수점 첫째 자리까지만 유지)
    selected_columns['체중'] = selected_columns['체중'].round(1)

    # 성별 전처리
    selected_columns['성별'] = selected_columns['성별'].map({'M': 0, 'F': 1})

    # 중성화 여부 전처리
    selected_columns['중성화 여부'] = selected_columns['중성화 여부'].map({'Y': 0, 'N': 1})

    # 최종 전처리된 컬럼 이름 변경
    selected_columns.rename(columns={
        '견종': 'final_견종',
        '나이': 'final_나이',
        '체중': 'final_체중',
        '성별': 'final_성별',
        '중성화 여부': 'final_중성화 여부',
        '입양여부': 'final_입양여부'
    }, inplace=True)

    processed_data = pd.concat([sampled_data.reset_index(drop=True), selected_columns.reset_index(drop=True)], axis=1)

    return processed_data

file_path = '../../resource/final_unadopted_data.csv'
processed_file_path = '../../resource/decision_tree_preprocessed_data/test_data/test_data_decision_tree_version2.csv'

# 데이터 전처리 및 저장
processed_data = preprocess_dog_data(file_path)
processed_data.to_csv(processed_file_path, index=False)
