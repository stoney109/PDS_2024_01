import pandas as pd
from datetime import datetime


'''

◆ 해당 파일에서 진행하는 데이터 전처리는 다음과 같습니다. ◆

1. 출생연도 데이터 전처리 : 날짜 형식을 YYYY.MM 형태로 통일

2. 보호 장소 데이터 정리 : 보호장소 형식을 서울특별시 + {지역명} 형태로 통일

3. 견종 및 세부견종 분리

4. 특징 데이터 추출 : 특징 열에서 특정 키워드를 기준으로 불필요한 정보를 제거 후 추출

5. 색상 데이터 추가 : '특징' 컬럼에서 특정 표현을 통해 추출, 알 수 없음은 'Unknown'으로 처리

6. 입양 여부 추가 : 서울동물복지지원센터 입양대기동물 현황의 api 데이터이므로, 모든 데이터에 입양여부를 N로 설정

7. 다른 데이터와 컬럼명 및 형태 통일

'''


# CSV 파일 경로 설정
input_csv_file = '../resource/crawing_data/seoul_crawling_20231116.csv'
output_csv_file = 'preprocessing_csv_files/seoul_base_preprocessing.csv'

# 데이터 불러오기
seoul_api_data = pd.read_csv(input_csv_file)


# 출생연도 컬럼의 날짜 데이터를 지정된 형식으로 변환
# seoul_api_data 데이터프레임의 '태어난년도' 열에 대해 반복문 적용
for i in range(len(seoul_api_data)):
    date_str = seoul_api_data['태어난년도'][i]

    # 문자열을 datetime 객체로 변환
    date_obj = datetime.strptime(date_str, '%Y/%m/%d %H:%M')

    # 새로운 형식의 문자열로 변환 (e.g. '2023.11')
    formatted_date = date_obj.strftime('%Y.%m')

    # 변환된 값으로 컬럼 값 업데이트
    seoul_api_data['태어난년도'][i] = formatted_date


# '보호 장소' 열의 값을 '서울특별시' + {x}의 형태로 통일 (e.g. 마포구 -> 서울특별시 마포구)
seoul_api_data['보호장소'] = seoul_api_data['보호장소'].apply(lambda x: '서울특별시' if '서울시' in str(x) else '서울특별시 ' + str(x))


# 새로운 '세부견종' 열 생성 및 데이터 분리
seoul_api_data['세부견종'] = ''

for i in range(len(seoul_api_data)):
    sample = seoul_api_data['종'][i]
    index_bracket = sample.find('(')  # 괄호 위치 찾기
    index_mix = sample.find('믹스')  # 믹스 키워드 위치 찾기

    # 괄호가 있는 경우 세부 견종 분리
    if index_bracket != -1:
        sub_breeds = sample[index_bracket + 1:-2].replace('믹스','')
        if '+' in sub_breeds:
            sub_breeds_list = sub_breeds.split('+')
            seoul_api_data['종'][i] = '믹스'
            seoul_api_data['세부견종'][i] = ', '.join(sub_breeds_list)
        elif '*' in sub_breeds:
            sub_breeds_list = sub_breeds.split('*')
            seoul_api_data['종'][i] = '믹스'
            seoul_api_data['세부견종'][i] = ', '.join(sub_breeds_list)
        else:
            seoul_api_data['종'][i] = '믹스'
            seoul_api_data['세부견종'][i] = sub_breeds
    # 믹스 키워드가 있는 경우
    elif index_mix != -1:
        seoul_api_data['종'][i] = '믹스'
        if seoul_api_data['종'][i] == '믹스':
            seoul_api_data['세부견종'][i] = '믹스'
        else:
            seoul_api_data['세부견종'][i] = sample[:index_mix]
    # 괄호와 믹스 키워드가 없는 경우
    else:
        seoul_api_data['세부견종'][i] = sample


# 특정 키워드를 기준으로 텍스트를 정리
for i in range(len(seoul_api_data)):
    sample = seoul_api_data['특징'][i]
    index_wait = sample.find('기다립니다.')
    index_marketing = sample.find('아이들과 자원봉사자님')

    # 두 가지 케이스에 대한 텍스트 분리
    if index_wait != -1:
      seoul_api_data['특징'][i] = sample[:index_wait+6]
    elif index_marketing != -1:
      seoul_api_data['특징'][i] = sample[:index_marketing]


# '특징'에서 색상 정보를 추출하여 새로운 '색상' 컬럼에 저장
for i in range(len(seoul_api_data)):
    sample = seoul_api_data['특징'][i]

    colors = []
    if sample.find('흰') != -1 or sample.find('하얀') != -1 or sample.find('화이트') != -1:
        colors.append('white')
    if sample.find('검정') != -1 or sample.find('검은') != -1  or sample.find('깜장') != -1 or sample.find('까만') != -1:
        colors.append('black')
    if sample.find('갈색') != -1 or sample.find('초코') != -1:
        colors.append('brown')
    if sample.find('베이지') != -1 or sample.find('노랑') != -1 or sample.find('노란') != -1:
        colors.append('beige')
    if sample.find('아이보리') != -1:
        colors.append('ivory')

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


# '입양여부' 컬럼 추가 : 서울동물복지지원센터 입양대기동물 현황의 api 데이터이므로 모두 N로 처리
seoul_api_data['입양여부'] = 'N'


# 불필요한 컬럼 삭제
seoul_api_data = seoul_api_data.drop(columns=['ID'])

# 일부 컬럼명 변경
seoul_api_data = seoul_api_data.rename(columns={
    '종': '견종',
    '태어난년도': '출생연도',
    '크기': '체중',
    '사진': '썸네일'
})


# 컬럼 순서 재배치
columns_order = ['이름', '견종', '세부견종', '색상', '출생연도',
                 '체중', '썸네일', '입양여부', '성별', '중성화여부', '특징', '보호장소']
seoul_api_data = seoul_api_data[columns_order]


# 최종 데이터프레임을 CSV로 저장
seoul_api_data.to_csv(output_csv_file, encoding='utf-8-sig', index=False)