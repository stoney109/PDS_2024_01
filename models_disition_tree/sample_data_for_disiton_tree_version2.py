#다른 방법의 전처리 방식
#샘플 데이터 (모델을 학습하기 위한 데이터)_apoted_data에서 추출
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

file_path = '../resource/final_unadopted_data.csv'

original_data = pd.read_csv(file_path)

# 성별이 Q 또는 중성화 여부가 U인 데이터 제외
filtered_data = original_data[
    (original_data['성별'] != 'Q') &
    (original_data['중성화 여부'] != 'U')
]

# 원본 데이터에서 랜덤으로 10,000건 추출 (필터링된 데이터 기준)
sampled_data = filtered_data.sample(n=10000, random_state=42)

# 필요한 컬럼만 추출
columns_to_select = ['견종', '나이', '체중', '성별', '중성화 여부', '입양여부']
selected_data = sampled_data[columns_to_select]

processed_data = selected_data.copy()

# 견종 처리: 믹스 -> 0, 그 외 -> 1
processed_data['견종'] = processed_data['견종'].apply(lambda x: 0 if '믹스' in str(x) else 1)

# 성별 처리: M -> 0, F -> 1
processed_data['성별'] = processed_data['성별'].apply(lambda x: 0 if x == 'M' else 1 if x == 'F' else x)

# 중성화 여부 처리: Y -> 0, N -> 1
processed_data['중성화 여부'] = processed_data['중성화 여부'].apply(lambda x: 0 if x == 'Y' else 1 if x == 'N' else x)

final_data = sampled_data.copy()
for column in processed_data.columns:
    final_data[f"전처리_{column}"] = processed_data[column]

#결과 저장
final_data.to_csv('sample_data/sample_data_disition_tree_version2.csv', index=False)
