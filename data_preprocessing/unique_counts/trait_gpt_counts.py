import pandas as pd
from collections import Counter

# 파일 경로
file_path = '../../resource/gpt_preprocessed_data/gpt_result_all_data.csv'

# 데이터 읽기
data = pd.read_csv(file_path, encoding='utf-8-sig')

# 'GPT_특성_변환' 컬럼에서 NaN 값 제거
data = data.dropna(subset=['GPT_특성_변환'])

# 쉼표로 나눈 후 평탄화
traits = data['GPT_특성_변환'].str.split(', ').explode()

# 특성별 빈도 계산
trait_counts = Counter(traits)

# 데이터프레임으로 변환
trait_counts_df = pd.DataFrame(trait_counts.items(), columns=['Trait', 'Count']).sort_values(by='Count', ascending=False)

# 결과 저장
trait_counts_df.to_csv('../trait_preprocessing/gpt_trait_counts.csv', encoding='utf-8-sig', index=False)

# 고유 특성 개수 출력
print(len(trait_counts_df))

# Count가 1인 데이터 제거
filtered_trait_counts_df = trait_counts_df[trait_counts_df['Count'] > 1]

# 남은 고유 특성 개수 출력
print(len(filtered_trait_counts_df))