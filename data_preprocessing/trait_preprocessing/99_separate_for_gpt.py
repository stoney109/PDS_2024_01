import pandas as pd

# CSV 파일 읽기
file_path = 'gpt_trait_data.csv'  # 파일 경로
df = pd.read_csv(file_path, encoding='utf-8-sig', low_memory=False)

# 상위 N번째 행부터 데이터 추출
# GPT api의 RPD 안에서 전처리한 데이터 개수 : 6280개 (gpt-3.5-turbo 기준 10,000 RPD)
end_n = 6280 # 끝 위치
result = df.iloc[:end_n]  # N번째 행부터 끝까지 추출

result.to_csv('separate_gpt_trait_data.csv', encoding='utf-8-sig', index=False)  # 결과 저장

print(f"추출된 데이터 행 수: {len(result)}")