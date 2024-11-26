import pandas as pd

# CSV 파일 경로 설정
input_csv_file = '../preprocessing_csv_files/nonglim_weight_preprocessing.csv'

# CSV 파일 읽기
df = pd.read_csv(input_csv_file)

# '중성화 여부' 컬럼에서 각 값의 개수 추출
unique_neutral_counts = df['중성화 여부'].value_counts().reset_index()
unique_neutral_counts.columns = ['중성화 여부', '개수']

# '중성화 여부' 종류 : Y/N/U
# '중성화 여부'와 개수 출력
print("'중성화 여부'와 각 개수:")
print(unique_neutral_counts.to_string(index=False))
