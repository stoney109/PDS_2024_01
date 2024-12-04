import pandas as pd

# CSV 파일 경로 설정
# 입력 : 전체 데이터 파일(input_csv_file)
# 출력 : 입양된 데이터 파일(output_csv_file_adopted), 입양되지 않은 데이터 파일(output_csv_file_unadopted)
input_csv_file = '../resource/result_all_data.csv'
output_csv_file_adopted = '../resource/final_adopted_data.csv'
output_csv_file_unadopted = '../resource/final_unadopted_data.csv'

# CSV 파일 읽기
data = pd.read_csv(input_csv_file, encoding='utf-8-sig')

# 입양된 데이터 필터링 : '입양여부'가 'Y'인 경우
adopted_data = data[data['입양여부'].str.contains('Y')].copy()

# 입양되지 않은 데이터 필터링 : '입양여부'가 'N'인 경우
unadopted_data = data[data['입양여부'].str.contains('N')].copy()

# 입양된 데이터와 입양되지 않은 데이터를 각각 새로운 CSV 파일로 저장
adopted_data.to_csv(output_csv_file_adopted, encoding='utf-8-sig', index=False)
unadopted_data.to_csv(output_csv_file_unadopted, encoding='utf-8-sig', index=False)

# 각 데이터셋의 개수 출력
num_adopted = len(adopted_data)
num_unadopted = len(unadopted_data)
print(f'입양된(Y) 강아지의 수: {num_adopted}개')
print(f'입양되지 않은(N) 강아지의 수: {num_unadopted}개')