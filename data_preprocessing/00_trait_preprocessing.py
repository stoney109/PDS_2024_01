import pandas as pd
from konlpy.tag import Okt
from hanspell import spell_checker
import re
import time
from multiprocessing import Pool, cpu_count
from tqdm import tqdm


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


# 명사, 형용사, 동사, 부사 필터링 함수
def extract_lemmas(text):
    if pd.notnull(text):
        # 텍스트에서 명사(Noun), 형용사(Adjective), 동사(Verb), 부사(Adverb)를 추출
        return [lemma for lemma, pos in okt.pos(text, norm=True, stem=True) if pos in ['Noun', 'Verb', 'Adjective', 'Adverb']]
    else:
        return []


# 병렬 처리 함수
def process_row(row):
    """
        1. 텍스트 정리
        2. 맞춤법 교정
        3. 형태소 추출
    """
    cleaned = clean_text(row)
    corrected = correct_spelling(cleaned)
    filtered = extract_lemmas(corrected)
    return cleaned, corrected, filtered


# 데이터 로드
data = pd.read_csv("../resource/final_adopted_data.csv", encoding='euc-kr', low_memory=False)

# 병렬 처리 시작
if __name__ == "__main__":
    with Pool(cpu_count()) as pool:
        results = list(tqdm(pool.imap(process_row, data['특징']), total=len(data)))

    # 결과 분리
    data['cleaned_text'], data['corrected_text'], data['filtered_text'] = zip(*results)

    # 전처리 결과 저장
    data.to_csv("preprocessing_csv_files/trait_preprocessing.csv", index=False, encoding='utf-8-sig')
