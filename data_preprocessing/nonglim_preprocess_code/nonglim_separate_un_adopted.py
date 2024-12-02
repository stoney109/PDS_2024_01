import pandas as pd

# CSV 파일 경로 설정
input_csv_file = '../preprocessing_csv_files/nonglim_weight_preprocessing.csv'
output_csv_file_adopted = '../preprocessing_csv_files/nonglim_adopted.csv'
output_csv_file_unadopted = '../preprocessing_csv_files/nonglim_unadopted.csv'

# CSV 파일 읽기 (ID와 접수일 열의 데이터 타입을 object로 설정)
data = pd.read_csv(input_csv_file, dtype={'접수일': 'object', '견종': 'object'})

# 입양된 데이터 필터링
adopted_data = data[data['입양여부'].str.contains(r'입양|기증')].copy()

# 입양되지 않은 데이터 필터링
unadopted_data = data[data['입양여부'].str.contains(r'안락사|자연사|보호중')].copy()

# '입양여부' 열 값을 'Y' 또는 'N'으로 변경
adopted_data['입양여부'] = 'Y'
unadopted_data['입양여부'] = 'N'

# 입양된 데이터와 입양되지 않은 데이터를 각각 새로운 CSV 파일로 저장
adopted_data.to_csv(output_csv_file_adopted, encoding='utf-8-sig', index=False)
unadopted_data.to_csv(output_csv_file_unadopted, encoding='utf-8-sig', index=False)

# 각 데이터셋의 개수 출력
num_adopted = len(adopted_data)
num_unadopted = len(unadopted_data)
print(f'입양된 강아지의 수: {num_adopted}개')
print(f'입양되지 않은 강아지의 수: {num_unadopted}개')