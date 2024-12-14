import pandas as pd

# CSV 파일 경로 설정
input_file_path = '../../resource/result_all_data.csv'

# CSV 파일 읽기
df = pd.read_csv(input_file_path, encoding='utf-8-sig')

# 길이를 계산할 텍스트 컬럼명 지정
# GPT api에 '특징' 문자열이 긴 순서대로 전처리를 진행하도록 하기 위해 해당 정렬을 활용했습니다.
target_text_column = '특징'

# 텍스트 길이 계산
df['text_length'] = df[target_text_column].astype(str).apply(len)

# 텍스트 길이 및 '썸네일' 컬럼 기준 정렬
df_sorted = df.sort_values(by=['text_length', '썸네일'], ascending=[False, True])

# 정렬 결과 길이 출력
print(len(df_sorted))

# 정렬된 결과를 CSV로 저장 : GPT api 활용시에 특성 텍스트가 많은 데이터 우선 활용
df_sorted.to_csv('sorted_result_all_data.csv', encoding='utf-8-sig', index=False)
