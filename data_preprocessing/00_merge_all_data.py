import pandas as pd

# 각 데이터 파일의 경로 설정
file_nonglim = "preprocessing_csv_files/nonglim_weight_preprocessing.csv"  # 농림 데이터 파일 경로
file_cafe = "preprocessing_csv_files/cafe_base_preprocessing.csv"  # 카페 데이터 파일 경로
file_seoul = "preprocessing_csv_files/seoul_base_preprocessing.csv"  # 서울 데이터 파일 경로

# 각 파일을 읽어 데이터프레임으로 변환
df_nonglim = pd.read_csv(file_nonglim)
df_cafe = pd.read_csv(file_cafe)
df_seoul = pd.read_csv(file_seoul)

# 공통 컬럼만 유지 : 분석에 필요한 공통 컬럼만 선택
common_columns = ['견종', '세부견종', '색상', '출생연도', '체중', '썸네일', '입양여부', '성별', '중성화 여부', '특징', '보호장소']

# 위의 공통 컬럼만 선택하여 각 데이터프레임 업데이트
df_nonglim = df_nonglim[common_columns]
df_cafe = df_cafe[common_columns]
df_seoul = df_seoul[common_columns]

# 세 데이터프레임을 하나로 병합
merged_df = pd.concat([df_nonglim, df_cafe, df_seoul], ignore_index=True)

# 중복 데이터 제거
df_before_dedup = len(merged_df)
merged_df = merged_df.drop_duplicates()
df_after_dedup = len(merged_df)

# 병합된 데이터를 CSV 파일로 저장
output_file = "../resource/result_all_data.csv"
merged_df.to_csv(output_file, index=False, encoding="utf-8-sig")

# 저장된 데이터의 총 행 개수를 출력합니다.
print(f"병합 완료! 총 {len(merged_df)}개의 데이터가 저장되었습니다.\n(중복 제거 전: {df_before_dedup} -> 중복 제거 후: {df_after_dedup})")

# 빈 문자열을 결측치로 대체 (None으로 변경)
merged_df.replace(r'^\s*$', None, regex=True, inplace=True)

# 각 컬럼의 결측치 개수 확인
print("\n◆ 각 컬럼의 결측치 개수 ◆")
print(merged_df.isnull().sum())
print("------------------------------")

# 데이터프레임 요약 정보 출력
print("\n◆ 데이터 요약 정보 ◆")
merged_df.info()
print("------------------------------")

# # 각 데이터프레임의 결측치 개수 확인 : 필요에 따라 주석 처리
# print("\n농림 데이터, 각 컬럼의 결측치 개수:")
# print(df_nonglim.isnull().sum())
# print("\n카페 데이터, 각 컬럼의 결측치 개수:")
# print(df_cafe.isnull().sum())
# print("\n서울 데이터, 각 컬럼의 결측치 개수:")
# print(df_seoul.isnull().sum())