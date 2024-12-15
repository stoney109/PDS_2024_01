import pandas as pd

# 파일 경로
file1 = '../../resource/decision_tree_preprocessed_data/test_data/test_data_decision_tree.csv'
file2 = '../../resource/decision_tree_preprocessed_data/sample_data/sample_data_decision_tree.csv'

# CSV 파일 읽기
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# 데이터프레임 병합 (행 방향)
merged_df = pd.concat([df1, df2], ignore_index=True)

# 결과 저장
output_file = '../../resource/decision_tree_preprocessed_data/merged_data/merged_data_version1.csv'
merged_df.to_csv(output_file, index=False)

