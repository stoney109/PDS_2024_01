import pandas as pd
from konlpy.tag import Okt
from hanspell import spell_checker
import re
import time
from tqdm import tqdm
from multiprocessing import Pool, cpu_count


r'''
본 코드는 특성 컬럼의 다양한 휴먼에러 전처리를 위하여, hanspell 라이브러리를 활용합니다.
해당 라이브러리 활용을 위하여, 아나콘다 프롬프트를 열고

pip3 install git+https://github.com/ssut/py-hanspell.git

위 구문을 입력하여 라이브러리를 수동 설치해주시길 바랍니다. 

*****

또한, 한글 자연어 처리를 위한 konlpy 라이브러리 사용에 JAVA의 설치가 필요합니다.
JAVA 8버전과 11버전에서는 해당 라이브러리가 정상작동하는 것을 확인하였으나, 21과 23 버전에서는 가상 머신 실행에 오류가 있음을 파악했습니다.

JAVA 설치 후 환경 변수를 설정하세요:
1. 윈도우 검색창에서 "시스템 환경 변수 편집" 검색 및 실행
2. 하단에 '환경 변수' 버튼 클릭
3. '시스템 변수' 섹션에서 '새로 만들기' 클릭
   - 변수 이름: JAVA_HOME
   - 변수 값: C:\Program Files\Java\jdk-11\bin\server
     ('jdk-11'부분은 설치 버전에 따라 폴더명이 달라질 수 있습니다.)
     (변수 값의 위치는 'jvm.dll' 파일이 존재하는 경로여야 정상작동합니다.)
4. 설정 후 '확인' 클릭

감사합니다.
'''


# 데이터 로드 및 저장 파일 이름 설정 함수 : 입양 Y/N 각 CSV 파일을 전처리한 후 저장
def process_file(input_file, output_file):
    """
        전처리할 CSV 파일(input_file)을 로드한 뒤 데이터 전처리를 수행하고,
        결과를 지정된 경로(output_file)에 저장하는 함수

        Parameters:
            input_file (str): 입력 CSV 파일 경로
            output_file (str): 전처리된 데이터를 저장할 출력 CSV 파일 경로
    """
    # 데이터 로드
    print(f"파일 전처리 시작: {input_file}")  # 시작 알림
    data = pd.read_csv(input_file, encoding='utf-8-sig', low_memory=False)

    # 병렬 처리 진행
    with Pool(cpu_count()) as pool:
        # 데이터 양이 많아 진행 상황을 실시간으로 확인하기 위해 tqdm으로 진행률 표시
        results = list(tqdm(pool.imap(process_row, data['특징']), total=len(data)))

    # 전처리 결과 분리 및 병합
    # 각 열에 대해 'cleaned_text', 'corrected_text', 'filtered_text' 데이터를 저장
    # TODO : 전처리 이후, 사용할 컬럼만 남기도록 코드 추가가 필요함
    data['cleaned_text'], data['corrected_text'], data['filtered_text'] = zip(*results)

    # 전처리 결과를 CSV 파일로 저장
    data.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"전처리 완료 파일 저장 경로: {output_file}\n")    # 완료 알림


# 형태소 분석기 초기화
okt = Okt()

# 텍스트 정리 함수 : 특수문자 및 연속 공백 제거
def clean_text(text):
    if pd.notnull(text):
        text = re.sub(r'[^가-힣\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return text


# 오타 교정 함수: hanspell 라이브러리 사용
spell_cache = {}    # 캐시 저장용 딕셔너리

def correct_spelling(text):
    if pd.notnull(text) and text.strip():  # 비어 있지 않은 경우에만 처리
        if text in spell_cache:
            return spell_cache[text]

        # 300자를 넘는 경우 300자 단위로 나눠 처리 : 네이버 맞춤법 검사기 활용 라이브러리이므로 300자로 나눠 검사하도록 코드 수정
        if len(text) > 300:
            parts = [text[i:i + 300] for i in range(0, len(text), 300)]
            corrected_parts = []
            for part in parts:
                try:
                    result = spell_checker.check(part)  # 맞춤법 검사
                    corrected_parts.append(result.checked)
                    time.sleep(0.3)  # 안정성을 위해 API 요청 딜레이
                except KeyError:
                    corrected_parts.append(part)   # 실패 시 원본 유지
                except Exception as e:
                    print(f"Error: {e} | Part: '{part}'")   # 에러 발생 시 해당 위치 출력
                    corrected_parts.append(part)
            corrected_text = ' '.join(corrected_parts)  # 처리된 결과 합치기
            spell_cache[text] = corrected_text  # 캐시에 저장
            return corrected_text

        # 300자 이하 텍스트 처리
        try:
            result = spell_checker.check(text)  # 맞춤법 검사
            spell_cache[text] = result.checked
            time.sleep(0.3)  # 안정성을 위해 API 요청 딜레이
            return result.checked
        except KeyError:
            return text  # API 호출 실패 시 원본 유지
        except Exception as e:
            print(f"Error: {e} | Text: '{text}'")   # 에러 발생 시 해당 위치 출력
            return text
    return text  # 빈 텍스트 그대로 반환


# 불용어 제거 함수
def remove_stopwords(lemmas, stopwords_lst):
    """
    형태소 리스트에서 불용어를 제거하는 함수

    Parameters:
        lemmas (list): 형태소 리스트
        stopwords_lst (list): 불용어 리스트

    Returns:
        list: 불용어가 제거된 형태소 리스트
    """
    return [lemma for lemma in lemmas if lemma not in stopwords_lst]


def extract_lemmas(text):
    """
       텍스트에서 명사, 형용사, 동사, 부사를 추출하고 불용어를 제거하는 함수

       Parameters:
           text (str): 처리할 텍스트 데이터

       Returns:
           list: 추출된 형태소에서 불용어가 제거된 리스트
    """
    if pd.notnull(text):
        # 텍스트에서 명사(Noun), 형용사(Adjective), 동사(Verb), 부사(Adverb)를 추출
        lemmas = [lemma for lemma, pos in okt.pos(text, norm=True, stem=True) if pos in ['Noun', 'Verb', 'Adjective', 'Adverb']]
        # 불용어 제거
        return remove_stopwords(lemmas, stopwords)
    else:
        return []   # 빈 텍스트는 빈 리스트 반환


def process_row(row):
    """
        위의 함수들을 실행하도록 하는 함수 : 각 실행 결과들은 해당 컬럼으로 저장
        다음과 같은 전처리 과정을 수행:
            1. 텍스트 정리 (clean_text)
            2. 맞춤법 교정 (correct_spelling)
            3. 형태소 추출 및 불용어 제거 (extract_lemmas)

        Parameters:
            row (str): 전처리할 텍스트 데이터

        Returns:
            tuple: (cleaned_text, corrected_text, filtered_text)
    """
    cleaned = clean_text(row)
    corrected = correct_spelling(cleaned)
    filtered = extract_lemmas(corrected)
    return cleaned, corrected, filtered


# 불용어 사전 : 전역 변수로 설정
stopwords = [
        # 색상 관련 단어 : 색깔, 색상 표현을 나타내는 불용어
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
        '와인', '와인색',

        # 일반 불용어
        '있다', '없다', '되다', '하다', '이다', '보임', '상태',
        '한', '그', '및', '하는', '하며', '부터', '까지',
        '것', '이런', '저런', '때문에', '위해', '가장',
        '매우', '모든', '다양한', '특히', '많은', '이', '저',
        '그것', '등', '위치', '크기', '종류', '상태', '등등', '따른', '대해', '추정'
    ]


if __name__ == "__main__":
    # 특성 전처리 대상 파일 경로, 전처리 후 저장 경로 설정
    files_to_process = [
        # 입양 Y 유기견 데이터
        ("../resource/final_adopted_data.csv", "preprocessing_csv_files/trait_adopted_preprocessing.csv"),
        # 입양 N 유기견 데이터
        ("../resource/final_unadopted_data.csv", "preprocessing_csv_files/trait_unadopted_preprocessing.csv")
    ]

    # 각 파일에 대해 전처리 실행
    for input_files, output_files in files_to_process:
        process_file(input_files, output_files)