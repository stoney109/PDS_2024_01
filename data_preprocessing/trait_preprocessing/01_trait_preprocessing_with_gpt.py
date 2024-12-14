import os
import time
import pandas as pd
from openai import OpenAI
from multiprocessing import Pool, cpu_count


'''
해당 파일은 OpenAI GPT 3.5 Turbo를 활용하여 입력 텍스트 데이터 전처리를 시도한 파일입니다.
텍스트 데이터의 주요 특성을 추출하고, 결과를 CSV 파일로 저장하는 기능을 제공합니다.

해당 파일을 제대로 작동시키기 위해서는, OpenAI사의 https://platform.openai.com/api-keys 페이지에 접속하여 
로그인과 프로젝트 설정 및 API key 발행과 토큰 충전이 필요합니다.
API key 발행 후에, '시스템 환경 변수 설정'에서 '시스템 변수' 섹션에서 '새로 만들기' 클릭
   - 변수 이름: OPENAI_API_KEY
   - 변수 값: sk-...IbIA
   (형태의 API key, 깃헙에 올리는 특성상 apikey의 노출 우려로 올리지 않았습니다. 필요하시다면, 이메일을 통해 apikey를 송부드리겠습니다.)

감사합니다.
'''


# API 클라이언트 설정
# OpenAI API를 사용하기 위해 클라이언트 객체 생성
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']
)

# 저장 주기 설정 : 데이터를 저장하는 행 간격
SAVE_INTERVAL = 10

# 입력 및 출력 CSV 파일 경로 설정
input_csv_file = 'sorted_result_all_data.csv'
output_csv_file = 'gpt_trait_data.csv'


# GPT를 활용한 전처리 함수
def gpt_preprocess_features(text):
    """
    입력 텍스트를 GPT를 활용해 전처리하는 함수

    Parameters:
        text (str): 전처리할 텍스트 데이터, 빈 문자열이나 NaN 값일 경우 처리하지 않음

    Returns:
            str: 전처리된 정제된 텍스트 데이터, 처리 실패 시 빈 문자열 반환
    """
    # 입력이 비어있거나 NaN일 경우 빈 문자열 반환
    if pd.isna(text) or text.strip() == "":
        return ""

    # # 텍스트 길이에 따라 max_tokens 동적으로 설정 : 데이터의 손실을 우려하여 우선 주석 처리
    # text_length = len(text)
    # max_tokens = (
    #     50 if text_length < 100 else
    #     150 if text_length < 500 else
    #     300 if text_length < 1000 else
    #     500 if text_length < 2000 else
    #     800
    # )

    # GPT에 전달할 메시지 생성 : 여러 차례 테스트 후 가장 안정적이고 정확한 결과를 도출한 프롬프트 사용
    # 텍스트의 핵심 특성을 추출하며, 불필요한 정보를 배제하도록 설계
    messages = [
        {
        "role": "system",
        "content": (
        "You are a text preprocessing assistant. Focus on extracting **concise traits** related to dogs. Follow these steps strictly."
        )
        },
        {
        "role": "user",
        "content": f"""
        **Rules**:
        1. Extract **key traits only**. Focus on personality, health, characteristics, and appearance.
        2. Do not include categories (e.g., '성격:', '건강:').
        3. Keep it **concise**. Remove unnecessary words, exaggerations, and embellishments.
        4. Use **single words whenever possible** for each trait. and convert adjectives to nominalized forms. Avoid phrases with 'XX가 XX함' or 'XX를 XX함'.
        5. **Output in Korean**, with traits listed and separated by a comma and a space.        

        **Input**:
        '{text}'
        
        **Output**:
        [List of concise traits in Korean, separated by commas]
                
        **Result**:
        """}
    ]

    # API 호출 최대 재시도 횟수 및 딜레이 설정 : 최대 5회 재시도하며, OpenAI API의 요청 제한(RPM, 분당 요청 수 제한)을 고려하여 30초 간격으로 재시도
    max_retries = 5
    retry_delay = 30  # 초 단위로 대기 시간 설정

    for attempt in range(max_retries):
        try:
            # OpenAI GPT 호출
            response = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = messages,
                # max_completion_tokens = max_tokens,
                temperature = 0.1,
                top_p = 0.3,
            )
            # 응답 내용 반환
            return response.choices[0].message.content.strip()

        except Exception as e:
            # Rate Limit 초과 시 재시도
            if "Error code: 429" in str(e):
                print(f"Error: {e}")
                print(f"Rate limit exceeded. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)  # 429 에러 시 대기
            # 다른 에러 발생 시 루프 탈출
            else:
                print(f"Error processing text: {text}\nError: {e}")
                break

    # 최대 재시도 횟수 초과 시 종료
    print(f"Failed to process text after {max_retries} retries: {text}")
    return ""  # 빈 문자열 반환


# 멀티프로세싱 실행 함수
def process_row(row):
    """
        데이터 행을 전처리하는 함수

        Parameters:
            row (tuple): 인덱스와 텍스트 데이터를 포함하는 튜플

        Returns:
            tuple: (인덱스, 전처리된 텍스트)
    """
    idx, feature = row
    try:
        return idx, gpt_preprocess_features(feature)
    except Exception as e:
        print(f"Error processing row {idx}: {e}")
        return idx, "ERROR"


# 데이터 저장 및 처리 함수
def process_csv(input_file, output_file, save_interval=10, num_workers=None):
    """
    CSV 파일을 로드해 GPT를 활용한 전처리를 수행하고 저장하는 함수

    Parameters:
        input_file (str): 입력 CSV 파일 경로
        output_file (str): 전처리된 데이터를 저장할 출력 CSV 파일 경로
        save_interval (int): 처리된 행 수가 save_interval에 도달할 때마다 데이터를 저장 (default는 10)
        num_workers (int, optional): 멀티프로세싱 워커(worker) 수 (default는 cpu_count()//2 : CPU 코어 개수의 절반)

    Returns:
        None: 함수는 처리 결과를 지정된 파일에 저장하며 반환값은 없음
    """
    try:
        # CSV 파일 로드
        data = pd.read_csv(input_file, encoding='utf-8-sig')

        # 빈 문자열을 결측치(None)로 대체 : NaN 처리를 통일
        data.replace(r'^\s*$', None, regex=True, inplace=True)

        # GPT 결과를 저장할 새로운 칼럼 추가
        data["GPT_특성"] = ""

        # "특징" 컬럼의 인덱스와 데이터를 튜플로 묶기
        rows = list(data["특징"].items())
        total_rows = len(rows)

        # 멀티프로세싱 설정
        processed_results = []
        with Pool(processes=num_workers or cpu_count()//2) as pool:
            for i, result in enumerate(pool.imap(process_row, rows), start=1):
                processed_results.append(result)

                # 저장 주기에 도달하면 중간 저장
                if i % save_interval == 0 or i == total_rows:
                    for idx, processed_feature in processed_results:
                        data.at[idx, "GPT_특성"] = processed_feature
                    data.to_csv(output_file, encoding='utf-8-sig', index=False)
                    print(f"◆◆ {i}/{total_rows} 행 저장 완료 ({(i / total_rows) * 100:.2f}% 완료) ◆◆")
                    processed_results = []

        print(f"전처리 완료. 결과가 {output_file}에 저장되었습니다.")

    except Exception as e:
        # CSV 파일 로드 및 전처리 중 예외 발생 시 오류 메시지 출력
        print(f"Failed to load CSV: {e}")
        return


# 실행
if __name__ == "__main__":
    process_csv(input_csv_file, output_csv_file, SAVE_INTERVAL, num_workers=10)
