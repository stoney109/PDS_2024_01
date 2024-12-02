import pandas as pd
import re
from datetime import datetime, timedelta


'''

◆ 해당 파일에서 진행하는 데이터 전처리는 다음과 같습니다. ◆

1. 출생연도 데이터 전처리:
   1) '들어온 날짜'와 '나이' 데이터를 기반으로 출생 연도를 추정하여 YYYY.MM 형식으로 통일.
   2) 데이터 형식이 맞지 않거나 계산이 불가능한 경우 'Unknown'으로 처리.

2. 보호 장소 데이터 정리 : 보호장소 형식을 서울특별시 + {지역명} 형태로 통일

3. 견종 및 세부견종 분리

4. 특징 데이터 정리 및 추출:
   - '특징' 컬럼에서 HTML 태그, 공백 등을 제거하여 텍스트를 정리.
   - 특정 키워드(예: '기다립니다.')를 기준으로 필요한 텍스트만 남김.

5. 색상 데이터 추가 : '특징' 컬럼에서 특정 표현을 통해 추출, 알 수 없음은 'Unknown'으로 처리

6. 입양 여부 추가 : 서울동물복지지원센터 입양대기동물 현황의 api 데이터이므로, 모든 데이터에 입양여부를 N로 설정

7. 중성화 여부 추가 : 중성화 상태를 알 수 없는 경우 모든 데이터를 'U'(Unknown)로 설정

8. 다른 데이터와 컬럼명 및 형태 통일

'''


# CSV 파일 경로 설정
input_csv_file = '../resource/crawing_data/seoul_crawling_20231116.csv'
output_csv_file = 'preprocessing_csv_files/seoul_base_preprocessing.csv'

# 데이터 불러오기
seoul_api_data = pd.read_csv(input_csv_file)


# # ID 컬럼에서 영어 문자가 포함된 행 삭제 : 해당 값을 확인 했을 때 오류 행으로 확인됨 >> 제거
seoul_api_data = seoul_api_data[~seoul_api_data['ID'].apply(lambda x: bool(re.search(r'[a-zA-Z]', str(x))))]


# '종' 컬럼에서 값이 'DOG'인 행만 유지 : 주제가 '유기견'이므로 기타 다른 동물 데이터에 대한 필터링
seoul_api_data = seoul_api_data[seoul_api_data['종'] == 'DOG'].reset_index(drop=True)


# '종' 컬럼의 'DOG' 값을 '믹스'로 변경 : 논의 필요, 알 수 없는 견종에 대해 '믹스'가 가장 많아 해당 전처리를 수행했던 것으로 추정
seoul_api_data['종'] = seoul_api_data['종'].replace('DOG', '믹스')


# '출생연도' 컬럼 생성
entry_dates = seoul_api_data['들어온 날짜']
ages = seoul_api_data['나이']
birth_years = []

for i in range(len(seoul_api_data)):
    try:
        # 들어온 날짜를 datetime 형식으로 변환
        entry_date = datetime.strptime(entry_dates[i], '%Y-%m-%d')

        # 나이 데이터에서 "세"와 "개월"을 추출
        age_info = ages[i]
        if '(' in age_info and ')' in age_info:
            # "2(세) 2(개월)" 형태에서 숫자를 추출
            try:
                age_years = int(age_info.split('(세)')[0].strip())
                age_months = int(age_info.split('(세)')[1].replace('(개월)', '').strip())
            except ValueError:
                # 숫자로 변환하지 못하면 'Unknown'으로 처리
                birth_years.append('Unknown')
                continue

            # 출생 날짜 계산
            birth_date = entry_date - timedelta(days=(age_years * 365 + age_months * 30.4))
            birth_year = birth_date.year
            birth_month = birth_date.month

            # 연도와 월 형식을 보정
            if birth_year < 100:  # 두 자리 연도일 경우
                birth_year = 2000 + birth_year

            birth_years.append(f"{birth_year}.{birth_month:02d}")  # YYYY.MM 형식
        else:
            # 나이 데이터 형식이 맞지 않을 경우 'Unknown' 처리
            birth_years.append('Unknown')

    except ValueError as e:
        # 들어온 날짜 형식이 잘못된 경우 예외 처리
        print(f"Date parsing error at row {i}: {e}")
        birth_years.append('Unknown')

# '출생연도' 컬럼 추가
seoul_api_data['출생연도'] = birth_years


# 보호장소 컬럼 추가
locations = []
for name in seoul_api_data['이름']:
    if '(' in name and '센터' in name:
        start_index = name.find('(') + 1  # 괄호 시작 위치
        end_index = name.find('센터')  # "센터" 이전 위치
        location = name[start_index:end_index] + '구'  # 추출된 지역명에 "구" 추가
        locations.append(location)
    else:
        locations.append('Unknown')  # 형식이 맞지 않는 경우

seoul_api_data['보호장소'] = locations


# '보호 장소' 열의 값을 '서울특별시' + {x}의 형태로 통일 (e.g. 마포구 -> 서울특별시 마포구)
seoul_api_data['보호장소'] = seoul_api_data['보호장소'].apply(lambda x: '서울특별시' if '서울시' in str(x) else '서울특별시 ' + str(x))


# '이름' 컬럼에서 ()와 그 안의 값 제거
seoul_api_data['이름'] = seoul_api_data['이름'].apply(lambda x: re.sub(r'\(.*?\)', '', x).strip())


# 새로운 '세부견종' 열 생성 및 데이터 분리
seoul_api_data['세부견종'] = ''

for i in range(len(seoul_api_data)):
    sample = seoul_api_data['종'][i]
    index_bracket = sample.find('(')  # 괄호 위치 찾기
    index_mix = sample.find('믹스')  # 믹스 키워드 위치 찾기

    # 괄호가 있는 경우 세부 견종 분리
    if index_bracket != -1:
        sub_breeds = sample[index_bracket + 1:-2].replace('믹스', '')
        if '+' in sub_breeds:
            sub_breeds_list = sub_breeds.split('+')
            seoul_api_data.loc[i, '종'] = '믹스'
            seoul_api_data.loc[i, '세부견종'] = ', '.join(sub_breeds_list)
        elif '*' in sub_breeds:
            sub_breeds_list = sub_breeds.split('*')
            seoul_api_data.loc[i, '종'] = '믹스'
            seoul_api_data.loc[i, '세부견종'] = ', '.join(sub_breeds_list)
        else:
            seoul_api_data.loc[i, '종'] = '믹스'
            seoul_api_data.loc[i, '세부견종'] = sub_breeds
    # 믹스 키워드가 있는 경우
    elif index_mix != -1:
        seoul_api_data.loc[i, '종'] = '믹스'
        if seoul_api_data.loc[i, '종'] == '믹스':
            seoul_api_data.loc[i, '세부견종'] = '믹스'
        else:
            seoul_api_data.loc[i, '세부견종'] = sample[:index_mix]
    # 괄호와 믹스 키워드가 없는 경우
    else:
        seoul_api_data.loc[i, '세부견종'] = sample


# '특징' 컬럼 내에 각종 HTML 태그 제거 및 연속된 공백 제거
seoul_api_data['특징'] = seoul_api_data['특징'].apply(
    lambda x: re.sub(r'<.*?>|&[a-z]+;|\uFEFF|\u200B', '', x)  # HTML 태그, 엔티티, ZWNBSP 제거
).apply(
    lambda x: re.sub(r'\s+', ' ', x)  # 연속된 공백을 단일 공백으로 대체
).str.strip()  # 앞뒤 공백 제거


# 특정 키워드를 기준으로 텍스트를 정리
for i in range(len(seoul_api_data)):
    sample = seoul_api_data['특징'][i]
    index_wait = sample.find('기다립니다.')
    index_marketing = sample.find('아이들과 자원봉사자님')

    # 두 가지 케이스에 대한 텍스트 분리
    if index_wait != -1:
        seoul_api_data.loc[i, '특징'] = sample[:index_wait + 6]
    elif index_marketing != -1:
        seoul_api_data.loc[i, '특징'] = sample[:index_marketing]


# '특징'에서 색상 정보를 추출하여 새로운 '색상' 컬럼에 저장
for i in range(len(seoul_api_data)):
    sample = seoul_api_data['특징'][i]

    colors = []
    if sample.find('흰') != -1 or sample.find('하얀') != -1 or sample.find('화이트') != -1:
        colors.append('White')
    if sample.find('검정') != -1 or sample.find('검은') != -1  or sample.find('깜장') != -1 or sample.find('까만') != -1:
        colors.append('Black')
    if sample.find('갈색') != -1 or sample.find('초코') != -1:
        colors.append('Brown')
    if sample.find('베이지') != -1 or sample.find('노랑') != -1 or sample.find('노란') != -1:
        colors.append('Beige')
    if sample.find('아이보리') != -1:
        colors.append('Ivory')

    # 추출된 색상 정보를 ', '로 연결
    color_string = ', '.join(colors)

    # '색상' 컬럼에 색상 정보 저장 (색상 정보가 없으면 'Unknown'으로 처리)
    seoul_api_data.at[i, '색상'] = color_string if color_string else 'Unknown'


# 특정 조건에 따라 색상 데이터 보완
# '종'이 말티즈이고, 색상이 비어 있으면 'White'로 설정
for i in range(len(seoul_api_data)):
    breed = seoul_api_data['종'][i].strip()
    sub_breed = seoul_api_data['세부견종'][i].strip()
    color = seoul_api_data['색상'][i]

    if breed == '말티즈' and sub_breed == '말티즈' and (pd.isna(color) or color == '' or color.lower() == 'none'):
        seoul_api_data.at[i, '색상'] = 'White'


# '입양여부' 컬럼 정보 수정 : 서울동물복지지원센터 입양대기동물 현황의 api 데이터이므로 모두 N로 처리
seoul_api_data['입양상태'] = 'N'


# '중성화여부' 컬럼 추가 : 데이터 자체에서 중성화 여부를 알 수 없으므로 Unknown 처리
seoul_api_data['중성화여부'] = 'U'


# 불필요한 컬럼 삭제
seoul_api_data = seoul_api_data.drop(columns=['ID'])


# 일부 컬럼명 변경
seoul_api_data = seoul_api_data.rename(columns={
    '종': '견종',
    '무게': '체중',
    '입양상태': '입양여부'
})


# 컬럼 순서 재배치
columns_order = ['이름', '견종', '세부견종', '색상', '출생연도',
                 '체중', '썸네일', '입양여부', '성별', '중성화여부', '특징', '보호장소']
seoul_api_data = seoul_api_data[columns_order]


# 최종 데이터프레임을 CSV로 저장
seoul_api_data.to_csv(output_csv_file, encoding='utf-8-sig', index=False)