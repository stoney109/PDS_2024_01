import pandas as pd
from datetime import datetime, timedelta

'''

◆ 해당 파일에서 진행하는 데이터 전처리는 다음과 같습니다. ◆

1. 데이터 병합

2. 특정 연도로 데이터 필터링 : 2020, 2021, 2022, 2023

3. 텍스트 데이터 정제
    1) 고양이 관련 단어가 포함된 행 삭제 >> 개 관련 데이터만 추출
    2) 특정 구간 텍스트 추출
    3) 불필요한 특수문자 제거

4. 새로운 컬럼 생성 : 텍스트 및 제목을 기반으로 필요한 정보 추출
    >> 이름, 보호장소, 견종, 성별, 중성화 여부, (추정나이 및 나이), 출생연도, 입양 여부

5. 불필요한 컬럼 삭제 : Unnamed: 0_x, Unnamed: 0_y, date, 제목, 텍스트, 나이, 나이_숫자 등

6. 입양 여부 추가 : 네이버 카페의 입양완료 게시판의 크롤링 데이터 이므로, 모든 데이터에 입양여부를 Y로 설정

7. 세부 견종 분리 및 데이터 형태 통일

8. 색상 데이터 추가 : '성격 및 기타 특징' 컬럼에서 특정 표현을 통해 추출, 알 수 없음은 'Unknown'으로 처리

9. 다른 데이터와 컬럼명 및 형태 통일

'''

# CSV 파일 경로 설정
input_csv_file = '../resource/crawing_data/cafe_crawling_20231116.csv'
output_csv_file = 'preprocessing_csv_files/cafe_base_preprocessing.csv'
cafe_date_csv_file = 'preprocessing_csv_files/cafe_date.csv'

# 데이터 불러오기 (UTF-8로 인코딩된 CSV 파일)
cafe_data = pd.read_csv(input_csv_file, encoding='utf-8')
cafe_dates = pd.read_csv(cafe_date_csv_file, encoding='utf-8')

# 데이터 병합 : 카페 입양완료 게시글 데이터와 해당 글의 날짜 데이터
data_cafe_craw = pd.merge(left=cafe_dates, right=cafe_data, left_index=True, right_index=True, how='inner')

# 불필요한 컬럼 제거
data_cafe_craw = data_cafe_craw.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'], axis=1)

# 'date' 컬럼에서 특정 연도로 시작하는 데이터만 필터링
data_cafe_craw = data_cafe_craw[data_cafe_craw['date'].str.startswith(('2020', '2021', '2022', '2023'))]

# 텍스트 데이터 정제 : 강아지 데이터 중심 활용이므로, 고양이 관련 단어가 있는 행 삭제
drop_indices = []
keywords_to_exclude = ['고양이', '묘종', '히말라얀', '페르시안', '터키시앙고라', '길냥이']
for idx, text in enumerate(data_cafe_craw['텍스트']):
    if any(keyword in text for keyword in keywords_to_exclude):
        drop_indices.append(idx)
data_cafe_craw = data_cafe_craw.drop(index=drop_indices).reset_index(drop=True)

# 텍스트 데이터 정제 : 특정 구간만 남기기
for idx, text in enumerate(data_cafe_craw['텍스트']):
    start_idx = text.find('이름')
    end_idx = text.find('입양절차안내 및 신청 바로가기(클릭)')
    extra_idx = text.find('충분히 고려해보신 후 입양신청해주세요')

    if start_idx != -1 and end_idx != -1:
        data_cafe_craw.at[idx, '텍스트'] = text[start_idx:end_idx]
    elif start_idx != -1:
        data_cafe_craw.at[idx, '텍스트'] = text[start_idx:]
    elif extra_idx != -1:
        data_cafe_craw.at[idx, '텍스트'] = text[extra_idx + len('충분히 고려해보신 후 입양신청해주세요'):]
    else:
        data_cafe_craw.at[idx, '텍스트'] = text

# 텍스트 정제: 불필요한 특수문자 제거
data_cafe_craw['텍스트'] = data_cafe_craw['텍스트'].apply(
    lambda text: text.replace("''", "")
    .replace(",", "")
    .replace("]", "")
    .replace("[", "")
    .replace("'", "")
    .replace("\\u200b", "")
    .replace("\\xa0", "")
)

# '이름' 칼럼 생성 (e.g. 쥬피(입양완료-2023.10.24 마포센터) -> '(' 앞의 '쥬피'만 추출)
for i in range(len(data_cafe_craw)):
    sample = data_cafe_craw['제목'][i]
    index_1 = sample.find('(')
    data_cafe_craw.at[i, '이름'] = sample[:index_1]

# '보호장소' 정보를 추가 (마포구, 동대문구, 구로구) : 텍스트 내에서 찾기
for i in range(len(data_cafe_craw)):
    sample = data_cafe_craw['텍스트'][i]
    index_1 = sample.find('마포')
    index_2 = sample.find('동대문')
    index_3 = sample.find('구로')

    if index_1 != -1:
        data_cafe_craw.at[i, '보호장소'] = '마포구'
    elif index_2 != -1:
        data_cafe_craw.at[i, '보호장소'] = '동대문구'
    elif index_3 != -1:
        data_cafe_craw.at[i, '보호장소'] = '구로구'

# '보호장소' 정보를 추가 (마포구, 동대문구, 구로구) : 제목 내에서 찾기
for i in range(len(data_cafe_craw)):
    sample = data_cafe_craw['제목'][i]
    index_1 = sample.find('마포')
    index_2 = sample.find('동대문')
    index_3 = sample.find('구로')

    if index_1 != -1:
        data_cafe_craw.at[i, '보호장소'] = '마포구'
    elif index_2 != -1:
        data_cafe_craw.at[i, '보호장소'] = '동대문구'
    elif index_3 != -1:
        data_cafe_craw.at[i, '보호장소'] = '구로구'
    else:
        data_cafe_craw.at[i, '보호장소'] = '서울시'

# '보호장소' 데이터 정리
data_cafe_craw['보호장소'] = data_cafe_craw['보호장소'].apply(
    lambda x: '서울특별시' if '서울시' in str(x) else f'서울특별시 {x}'
)

# '견종' 데이터 정제
not_form = []
for i in range(len(data_cafe_craw)):
    sample = data_cafe_craw['텍스트'][i]
    name = data_cafe_craw['이름'][i]
    index_1 = sample.find(name)
    index_2 = sample.find('성별')
    index_3 = sample.find('견종')
    index_5 = sample.find('품종')
    index_4 = sample.find(' / ')

    if index_1 != -1 and index_2 != -1:
        data_cafe_craw.at[i, '견종'] = sample[index_1:index_2]
    elif index_2 != -1 and index_3 != -1:
        data_cafe_craw.at[i, '견종'] = sample[index_3:index_2]
    elif index_3 != -1:
        data_cafe_craw.at[i, '견종'] = sample[index_3:index_2]
    elif index_2 != -1 and index_5 != -1:
        data_cafe_craw.at[i, '견종'] = sample[index_5:index_2]
    else:
        not_form.append(i)
        data_cafe_craw.at[i, '견종'] = sample

# '견종' 열에서 빈 문자열을 NaN으로 변환
data_cafe_craw['견종'] = data_cafe_craw['견종'].replace('', pd.NA)

# '견종' 열에서 NaN 값이 있는 행을 찾기
rows_with_null = data_cafe_craw[data_cafe_craw['견종'].isnull()]

# '견종' 열의 NaN 행을 처리하여 데이터 보완
for index, row in rows_with_null.iterrows():
    text = row['텍스트']
    index_breed = text.find('견종')
    index_sex = text.find('성별')

    # '견종'과 '성별' 사이 텍스트 추출
    if index_breed != -1 and index_sex != -1:
        data_cafe_craw.at[index, '견종'] = text[index_breed:index_sex]
    elif index_sex != -1:
        # '견종'이 없고 '성별'만 있다면 '성별' 이후 텍스트를 추가
        data_cafe_craw.at[index, '견종'] = text[index_sex:]

# '견종' 데이터에서 ':' 뒤의 텍스트를 남기고 나머지 제거
for i in range(len(data_cafe_craw)):
    sample = data_cafe_craw['견종'][i]
    name = data_cafe_craw['이름'][i]
    if ':' in sample:
        data_cafe_craw.at[i, '견종'] = sample.split(':')[1]
    else:
        data_cafe_craw.at[i, '견종'] = sample

# '성별' 정보를 '텍스트'에서 추출
for i in range(len(data_cafe_craw)):
    sample = data_cafe_craw['텍스트'][i]
    index_1 = sample.find('성별')
    index_2 = sample.find('추정나이')

    if index_1 != -1 and index_2 != -1:
        data_cafe_craw.at[i, '성별'] = sample[index_1 + 5:index_2]

# '성격 및 기타 특징' 정보를 '텍스트'에서 추출
for i in range(len(data_cafe_craw)):
    sample = data_cafe_craw['텍스트'][i]
    index_1 = sample.find('성격 및 기타 특징')
    index_2 = sample.find('기다립니다.')  # 양식 상 유튜브 링크가 나오기 전까지

    if index_1 != -1 and index_2 != -1:
        data_cafe_craw.at[i, '성격 및 기타 특징'] = sample[index_1 + 12: index_2 + 6]

# '성별' 열에서 중성화 여부를 파악하여 추가
for i in range(len(data_cafe_craw)):
    sample = data_cafe_craw['성별'][i]
    index_1 = sample.find('(중성화O)')
    index_2 = sample.find('중성화된')
    index_3 = sample.find('미중성')

    if index_1 != -1 or index_2 != -1:
        # 중성화된 경우
        data_cafe_craw.at[i, '중성화 여부'] = 'Y'
    elif index_3 != -1:
        # 중성화되지 않은 경우
        data_cafe_craw.at[i, '중성화 여부'] = 'N'
    else:
        # 알 수 없는 경우
        data_cafe_craw.at[i, '중성화 여부'] = 'U'

# '성별' 정보를 간소화 (암컷 -> F, 수컷 -> M, 알 수 없음 -> Q)
for i in range(len(data_cafe_craw)):
    sample = data_cafe_craw['성별'][i]

    if '암컷' in sample:
        data_cafe_craw.at[i, '성별'] = 'F'
    elif '수컷' in sample:
        data_cafe_craw.at[i, '성별'] = 'M'
    else:
        data_cafe_craw.at[i, '성별'] = 'Q'

# '추정나이' 정보를 '텍스트'에서 추출
for i in range(len(data_cafe_craw)):
    sample = data_cafe_craw['텍스트'][i]
    index_1 = sample.find('추정나이')
    index_2 = sample.find('성격')

    if index_1 != -1 and index_2 != -1:
        data_cafe_craw.at[i, '나이'] = sample[index_1 + 4:index_2].replace(" ", '').replace(":", '').replace('현재', '')

# 현재 연도를 기준으로 출생 연도를 계산하고 '나이' 정보를 업데이트
current_year = datetime.now().year
for i in range(len(data_cafe_craw)):
    sample = data_cafe_craw['나이'][i]
    index_1 = sample.find('출생')

    if index_1 != -1:
        cleaned_sample = sample.replace('출생', '')
        # 출생 날짜 변환
        birth_date = datetime.strptime(cleaned_sample, '%Y.%m.%d')
        age_in_days = (datetime.now() - birth_date).days
        age = age_in_days / 365.25  # 나이를 연 단위로 계산
        data_cafe_craw.at[i, '출생연도'] = birth_date.strftime('%Y.%m')
        data_cafe_craw.at[i, '나이'] = round(age, 1)

# 'data_cafe_craw' 데이터프레임에서 '나이' 컬럼을 기반으로 출생연도를 계산
# 나이는 변동, 출생연도는 변동하지 않음으로 전체 데이터에서 출생연도를 기반으로 하기로 결정
for i in range(len(data_cafe_craw)):
    # '나이' 컬럼에서 각 데이터를 가져옴
    sample = data_cafe_craw['나이'][i]

    # 데이터가 숫자(float)가 아닌 경우에만 처리 (즉, 문자열 형태일 때 실행)
    if not isinstance(sample, float):
        index_age_1 = sample.find('살')
        index_age_2 = sample.find('개월')
        index_age_3 = sample.find('세')
        index_year = sample.find('출생')

        # 'date' 컬럼 값을 datetime 객체로 변환
        date_str = data_cafe_craw['date'][i]
        date_format = "%Y.%m.%d."
        date_obj = datetime.strptime(date_str, date_format)

        if index_year != -1:
            # '출생' 키워드가 있을 경우, '출생' 이후의 정보를 '출생연도' 컬럼에 저장
            data_cafe_craw.at[i, '출생연도'] = sample[index_year + 2:]
        elif index_age_1 != -1:
            # 나이('n살') 정보를 추출하여 현재 날짜에서 해당 연수를 빼서 출생연도 계산
            years_to_subtract = int(sample[:index_age_1])
            new_date = date_obj - timedelta(days=365 * years_to_subtract)
            data_cafe_craw.at[i, '출생연도'] = new_date.strftime('%Y.%m')
        elif index_age_3 != -1:
            # 나이('n세') 정보를 추출하여 현재 날짜에서 해당 연수를 빼서 출생연도 계산
            years_to_subtract = int(sample[:index_age_3])
            new_date = date_obj - timedelta(days=365 * years_to_subtract)
            data_cafe_craw.at[i, '출생연도'] = new_date.strftime('%Y.%m')
        elif index_age_2 != -1:
            # 나이('n개월') 정보를 추출하여 현재 날짜에서 해당 개월 수를 빼서 출생연도 계산
            months_to_subtract = int(sample[:-2])
            new_date = date_obj - timedelta(days=30 * months_to_subtract)
            data_cafe_craw.at[i, '출생연도'] = new_date.strftime('%Y.%m')
        else:
            # 위 조건 중 어느 것도 해당되지 않는 경우, 기존 '출생연도' 값 유지
            data_cafe_craw.at[i, '출생연도'] = data_cafe_craw.at[i, '출생연도']

# '성격 및 기타 특징'에서 URL 제거
for i in range(len(data_cafe_craw)):
    sample = data_cafe_craw['성격 및 기타 특징'][i]
    if isinstance(sample, str):  # 문자열인지 확인
        index_trait = sample.find('http')
        if index_trait != -1:
            # http 이후 한글 문자가 나오는 위치 탐색
            for j in range(index_trait, len(sample)):
                if '\uAC00' <= sample[j] <= '\uD7A3':  # 한글 문자 확인
                    # http부터 한글 문자 바로 직전까지의 부분을 제거
                    data_cafe_craw.at[i, '성격 및 기타 특징'] = sample[:index_trait] + sample[j:]
                    break

# '나이' 열을 숫자로 변환하고 새로운 열 생성
data_cafe_craw['나이_숫자'] = data_cafe_craw['나이'].str.extract(r'(\d+)').astype(float)
data_cafe_craw['나이_조정'] = data_cafe_craw.apply(
    lambda row: row['나이'] if pd.isna(row['나이_숫자']) else round(row['나이_숫자'] / 12, 1) if '개월' in row['나이'] else row[
        '나이_숫자'],
    axis=1)

# 불필요한 열 삭제
columns_to_drop = ['date', '제목', '텍스트', '나이', '나이_숫자']
data_cafe_craw = data_cafe_craw.drop(columns=columns_to_drop, axis=1)

# '나이_조정' 컬럼을 '나이'로 변경
data_cafe_craw.rename(columns={'나이_조정': '나이'}, inplace=True)

# '입양여부' 열 추가 : 네이버 카페의 입양완료 게시판의 크롤링 데이터 이므로 모두 Y로 처리
data_cafe_craw['입양여부'] = 'Y'

# '세부견종' 열 추가 및 초기화
data_cafe_craw['세부견종'] = ''


# '견종' 데이터를 기반으로 '세부견종' 분리 함수 정의
def extract_sub_breeds(row):
    sample = row['견종']
    index_bracket = sample.find('(')  # 괄호 위치 찾기
    index_mix = sample.find('믹스')  # 믹스 키워드 위치 찾기

    # 괄호가 있는 경우 세부 견종 분리
    if index_bracket != -1:
        sub_breeds = sample[index_bracket + 1:-2].replace('믹스', '')
        if '+' in sub_breeds:
            return '믹스', ', '.join(sub_breeds.split('+'))
        elif '*' in sub_breeds:
            return '믹스', ', '.join(sub_breeds.split('*'))
        else:
            return '믹스', sub_breeds
    # 믹스 키워드가 있는 경우
    elif index_mix != -1:
        return '믹스', '믹스' if sample == '믹스' else sample[:index_mix]
    # 괄호와 믹스 키워드가 없는 경우
    else:
        return sample, sample


# '견종'과 '세부견종' 분리 적용
data_cafe_craw[['견종', '세부견종']] = data_cafe_craw.apply(lambda row: pd.Series(extract_sub_breeds(row)), axis=1)

# '견종' 컬럼의 오타 수정을 위한 전처리
data_cafe_craw['견종'] = data_cafe_craw['견종'].str.replace(r'\s+', '', regex=True)

# '견종' 컬럼의 오타 수정 및 형태 통일
cleaned_breeds = {
    '폼': '폼피츠',
    '보스턴 테이어': '보스턴테리어',
    '포메라이안': '포메라니안',
    '포메라이니안': '포메라니안',
    '시추': '시츄',
    '미니핀': '미니어쳐핀셔',
}
data_cafe_craw['견종'] = data_cafe_craw['견종'].replace(cleaned_breeds)

# '세부견종'에서 불필요한 문자 제거 및 정리
data_cafe_craw['세부견종'] = (
    data_cafe_craw['세부견종']
    .str.replace('[)?]', '', regex=True)  # ')'와 '?' 제거
    .str.replace('(추정|혼종)', '', regex=True)  # '추정', '혼종' 제거
    .str.replace(r'\s', '', regex=True)  # 띄어쓰기 제거 (정규식 사용ㅇ)
    .str.replace('.*=', '', regex=True)  # '=' 포함 문자열 제거
)

# '세부견종'의 일부 데이터를 통일된 이름으로 대체
replace_dict = {
    '폼': '폼피츠',
    '보스턴 테이어': '보스턴테리어',
    '포메라이안': '포메라니안',
    '포메라이니안': '포메라니안',
    '시추': '시츄',
    '미니핀': '미니어쳐핀셔',
    '푸숑': '비숑프리제, 푸들',
    '폼피츠,페키니즈': '포메라니안, 페키니즈',
    '폼피츠|포메라니안,스피츠': '포메라니안, 스피츠',
    '말티즈,시추': '말티즈, 시츄',
    '말티즈,푸들': '말티즈, 푸들',
    '비숑,푸들': '비숑프리제, 푸들',
    '코카스파니엘,푸들': '코카스파니엘, 푸들'
}
data_cafe_craw['세부견종'] = data_cafe_craw['세부견종'].replace(replace_dict)

# '세부견종' 컬럼의 값이 NaN, 공백, 또는 빈 문자열일 경우 NaN으로 변환
data_cafe_craw['세부견종'] = data_cafe_craw['세부견종'].replace(r'^\s*$', pd.NA, regex=True)

# '견종'이 '믹스'이고 '세부견종'이 비어있다면 '세부견종'을 '믹스'로 채우기
data_cafe_craw.loc[(data_cafe_craw['견종'] == '믹스') & (data_cafe_craw['세부견종'].isnull()), '세부견종'] = '믹스'

# '성격 및 기타 특징'컬럼 에서 색상 정보 추출
for i in range(len(data_cafe_craw)):
    sample = data_cafe_craw['성격 및 기타 특징'][i]
    colors = []

    # sample이 문자열인 경우에만 처리
    if isinstance(sample, str):
        if sample.find('흰') != -1 or sample.find('하얀') != -1 or sample.find('화이트') != -1:
            colors.append('White')
        if sample.find('검정') != -1 or sample.find('검은') != -1 or sample.find('깜장') != -1 or sample.find('까만') != -1:
            colors.append('Black')
        if sample.find('갈색') != -1 or sample.find('초코') != -1:
            colors.append('Brown')
        if sample.find('베이지') != -1 or sample.find('노랑') != -1 or sample.find('노란') != -1:
            colors.append('Beige')
        if sample.find('아이보리') != -1:
            colors.append('Ivory')

    # 추출된 색상 정보를 ', '로 연결하여 저장
    color_string = ', '.join(colors)

    # '색상' 컬럼에 색상 정보 저장 (색상 정보가 없으면 'Unknown'으로 처리)
    data_cafe_craw.at[i, '색상'] = color_string if color_string else 'Unknown'

# 특정 조건에 따라 색상 데이터 보완
# '종'이 말티즈이고, 색상이 비어 있으면 'White'로 설정
for i in range(len(data_cafe_craw)):
    breed = data_cafe_craw['견종'][i].strip()
    sub_breed = data_cafe_craw['세부견종'][i].strip()
    color = data_cafe_craw['색상'][i]

    if breed == '말티즈' and sub_breed == '말티즈' and pd.isna(color):
        data_cafe_craw.at[i, '색상'] = 'White'

# 카페 게시글에서는 체중에 대한 정확한 수치를 확인 불가
# 평균값을 해치지 않기 위해 7.16 kg으로 값을 할당 (총 231개의 데이터)
data_cafe_craw['체중'] = 7.16

# 모든 문자열 컬럼에 대해 strip 적용
for col in data_cafe_craw.select_dtypes(include=['object']).columns:  # 문자열 데이터 타입 선택
    data_cafe_craw[col] = data_cafe_craw[col].map(lambda x: x.strip() if isinstance(x, str) else x)

# '성격 및 기타 특징' 컬럼명을 '특징'으로 변경
data_cafe_craw = data_cafe_craw.rename(columns={'성격 및 기타 특징': '특징'})

# 컬럼 순서 재배치
columns_order = ['이름', '견종', '세부견종', '색상', '출생연도', '나이', '체중', '썸네일',
                 '입양여부', '성별', '중성화 여부', '특징', '보호장소']
data_cafe_craw = data_cafe_craw[columns_order]

# 최종 데이터프레임을 CSV로 저장
data_cafe_craw.to_csv(output_csv_file, encoding='utf-8-sig', index=False)

# 처리된 요소 수 출력
num_elements = len(data_cafe_craw)
print(f'처리된 데이터의 수: {num_elements}개')

print(data_cafe_craw.isnull().sum())