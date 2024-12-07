import csv
from konlpy.tag import Okt

# # 혹시 모를 인코딩이 통일되지 않을 때를 대비하여 CSV 파일의 인코딩을 euc-kr에서 utf-8로 변환하는 함수
# def convert_csv_encoding(input_file_path, output_file_path):
#     # euc-kr로 파일 읽기
#     df = pd.read_csv(input_file_path, encoding='euc-kr', low_memory=False)
#     # utf-8로 파일 재저장
#     df.to_csv(output_file_path, index=False, encoding='utf-8')

# 주어진 텍스트에서 불용어를 제거하고 중요한 형태소만 추출하는 함수
def extract_important_morphs(text, stopwords):
    okt = Okt()  # Okt 형태소 분석기 객체 생성
    morphs = okt.morphs(text)  # 텍스트를 형태소 단위로 분리
    # 불용어 목록에 포함되지 않은 형태소만 필터링
    filtered_morphs = [morph for morph in morphs if morph not in stopwords]
    return filtered_morphs  # 필터링된 형태소 리스트 반환

# 강아지 이름과 특성을 처리하는 함수
def process_dog_traits(data_a, data_b, stopwords):
    processed_data = []  # 처리된 데이터를 저장할 리스트

    # 이름(name)과 특성(trait)을 하나씩 반복
    for name, trait in zip(data_a, data_b):
        # 특성을 형태소 분석하고 불용어 제거
        important_morphs = extract_important_morphs(trait, stopwords)
        # 이름과 처리된 특성을 튜플 형태로 리스트에 추가
        processed_data.append((name, important_morphs))

    return processed_data  # 처리된 데이터 리스트 반환

# CSV 파일에서 데이터를 읽어오는 함수
def read_csv(file_path, name_column_index, trait_column_index):
    names = []  # 이름 데이터를 저장할 리스트
    traits = []  # 특성 데이터를 저장할 리스트

    # CSV 파일 열기
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)  # CSV 파일 읽기
        for row in reader:  # 파일의 각 행(row)을 반복
            # 지정된 열의 데이터를 각각 이름과 특성 리스트에 추가
            names.append(row[name_column_index])
            traits.append(row[trait_column_index])

    return names, traits  # 이름 리스트와 특성 리스트 반환

# 처리된 데이터를 새로운 CSV 파일에 저장하는 함수
def save_to_csv(data, output_file_path):
    # CSV 파일 쓰기 모드로 열기
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)  # CSV 작성기 생성
        writer.writerow(['Name', 'Processed_Traits'])  # 헤더(열 제목) 작성

        # 처리된 데이터의 각 튜플(name, traits)을 파일에 기록
        for name, traits in data:
            # 형태소 리스트를 공백으로 연결하여 한 문자열로 변환
            writer.writerow([name, ' '.join(traits)])

##인코딩 함수 연관부분(위에 주석 풀면서 같이 풀어야 함)
# # CSV 파일 경로 설정
# original_csv_file_path = '../../resource/final_adopted_data.csv'
# utf8_csv_file_path = '../../resource/final_adopted_data_utf8.csv'
#
# # 원본 파일을 euc-kr에서 utf-8로 변환
# convert_csv_encoding(original_csv_file_path, utf8_csv_file_path)

# CSV 파일에서 이름과 특성 데이터 읽어오기

csv_file_path = '../../data_preprocessing/preprocessing_csv_files/trait_unadopted_preprocessing.csv'

name_column_index = 0  # 이름이 있는 열의 인덱스
trait_column_index = 15  # 특성 데이터가 있는 열의 인덱스
names_a, traits_b = read_csv(csv_file_path, name_column_index, trait_column_index)

# 불용어 리스트 설정 (분석에서 제외할 단어들)
stopwords = [
    '.', '을', '이', ',', '에', '가', '를', '도', '의', '으로', '는', '강아지', '가족', '가정',
    '잘', '들', '사람', '~', '!', '하는', '등', '과', '은', '는', '있는', '센터', '한', '다른',
    '입니다', '하고', '후', '예요', '로', '에서', '어느', '해', '너무', '수', '에게', '아델', '것',
    '와', '있습니다', '있어요', '.', '(', '요', '합니다', '듯', '중', '되어', '또는', '(', '고',
    '화', '.)', '라', '인', ')', '할', '과도', '라서', '^^', '때', '이며', '하지만', '아', '곳',
    '더', '하면', '면', '이나', '부터', '때문', 'kg', '했습니다', '이지만', '했어요', '또한',
    '엉', '있었어요', '해주세요', '있어', '했으며', '됩니다','있다', '없다', '되다', '하다', '이다', '보임', '상태',
    '한', '그', '및', '하는', '하며', '부터', '까지',
    '것', '이런', '저런', '때문에', '위해', '가장',
    '매우', '모든', '다양한', '특히', '많은', '저',
    '그것', '위치', '크기', '종류', '상태', '등등', '따른', '대해','추정','다',

    # 색상 관련 단어
    '색상', '색깔', '색',
    '빨강', '빨간색', '빨간', '빨갛다',
    '주황', '주황색', '주홍색', '주홍',
    '노랑', '노란색', '노란', '노랗다',
    '초록', '초록색', '초록빛', '연두', '연두색', '초록빛', '초록하다',
    '파랑', '파란색', '파란', '하늘색', '남색', '청색', '파랗다', '푸르다',
    '보라', '보라색', '자주', '자주색',
    '흰색', '하얀', '하얀색', '백색', '하얗다',
    '검정', '검은', '검정색', '까만', '까만색', '검다',
    '회색', '회빛',
    '갈색', '브라운', '갈색빛',
    '분홍', '분홍색', '핑크',
    '금색', '황금색', '황색', '금빛',
    '은색', '은빛',
    '다홍', '다홍색',
    '아이보리', '아이보리색',
    '베이지', '베이지색',
    '민트', '민트색',
    '초코색', '초콜릿색',
    '청록색', '카키', '카키색',
    '와인', '와인색'
]

# 각각의 강아지 특성을 형태소 단위로 토큰화하고 중요한 형태소 추출
processed_dog_traits = process_dog_traits(names_a, traits_b, stopwords)

# 결과를 CSV 파일로 저장
output_csv_file_path = '../../resource/text_preprocessing_traits/unadopted_text_cleaning_by_morphs.csv'
save_to_csv(processed_dog_traits, output_csv_file_path)