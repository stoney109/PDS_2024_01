from transformers import AutoTokenizer, AutoModelForSequenceClassification
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import pandas as pd
import torch


"""
이 파일은 사전 학습된 KoBERT 모델을 사용하여 텍스트 데이터에 대해 감성 분석을 수행합니다.

주요 기능:
    1. 텍스트 데이터를 긍정(Positive), 부정(Negative), 중립(Neutral)으로 분류
    2. 입력 데이터(CSV 파일)를 로드하고, 텍스트 데이터를 전처리
    3. 병렬 처리를 통해 감성 분석 작업을 최적화
    4. 분석 결과를 데이터프레임에 추가하고, 결과를 CSV 파일로 저장
"""


def analyze_text_sentiment(args):
    """
    리스트 형태의 텍스트 데이터를 입력받아 각 요소에 대해 감성 분석을 수행
    Positive, Negative, Neutral 개수를 반환

    Args:
        args (tuple): 텍스트 리스트, tokenizer 객체, model 객체

    Returns:
        tuple: positive_count, negative_count, neutral_count
    """
    text_list, tokenizer, model = args
    positive_count = 0  # 긍정적 감정의 개수
    negative_count = 0  # 부정적 감정의 개수
    neutral_count = 0   # 중립적 감정의 개수

    for segment in text_list:
        # 텍스트의 공백 제거, 빈 문자열인 경우 중립 처리
        segment = segment.strip()
        if not segment:
            neutral_count += 1
            continue

        # 입력 텍스트를 토크나이저를 통해 토큰화하고 모델에 적합한 입력 텐서로 변환
        inputs = tokenizer(segment, return_tensors="pt", truncation=True, padding=True, max_length=128)
        with torch.no_grad():  # 추론 모드 활성화 (기울기 계산을 비활성화하여 메모리 사용 최적화)
            outputs = model(**inputs)  # 모델을 통해 예측 수행
        logits = outputs.logits  # 로짓 값 추출
        probabilities = torch.softmax(logits, dim=-1).squeeze().tolist()  # 각 클래스 확률 계산
        sentiment = torch.argmax(logits, dim=-1).item()  # 예측된 감성 클래스 (0: Negative, 1: Positive)

        # 두 감정 확률의 차이가 0.2 미만인 경우, 중립으로 간주
        if abs(probabilities[1] - probabilities[0]) < 0.2:
            neutral_count += 1
        elif sentiment == 1:
            positive_count += 1
        else:
            negative_count += 1

    return positive_count, negative_count, neutral_count


def parallel_sentiment_analysis(text_data, tokenizer, model):
    """
    데이터프레임 내 텍스트 데이터에 병렬 처리로 감성 분석 수행

    Args:
        text_data (pd.Series): 분석 대상 텍스트 데이터 시리즈
        tokenizer (transformers.AutoTokenizer): 텍스트 토크나이저 객체
        model (transformers.AutoModelForSequenceClassification): 감성 분석 모델 객체

    Returns:
        list: 각 텍스트에 대한 감성 분석 결과 리스트
    """
    # 텍스트 데이터와 모델을 튜플로 묶어 병렬 처리에 전달
    data_with_model = [(text, tokenizer, model) for text in text_data]
    with Pool(cpu_count()) as pool:  # CPU 코어 수만큼 병렬 처리
        # 병렬 작업 진행 및 진행 상황 표시 (tqdm 활용)
        results = list(tqdm(pool.imap(analyze_text_sentiment, data_with_model), total=len(text_data)))
    return results


if __name__ == "__main__":
    # 사전 학습된 모델과 토크나이저 로드
    tokenizer = AutoTokenizer.from_pretrained("beomi/kcbert-large")
    model = AutoModelForSequenceClassification.from_pretrained("beomi/kcbert-large", num_labels=2)

    # 감성 분석 대상 텍스트 데이터를 포함한 CSV 파일 로드
    input_file_path = "../../resource/gpt_preprocessed_data/gpt_result_all_data.csv"  # CSV 파일 경로
    df = pd.read_csv(input_file_path, encoding='utf-8-sig')

    # GPT_특성을 쉼표로 나눠 리스트로 변환
    df["GPT_특성"] = df["GPT_특성"].fillna("").apply(lambda x: [i.strip() for i in x.split(",") if i.strip()])

    # 병렬 감성 분석 수행
    sentiment_analysis_results = parallel_sentiment_analysis(df["GPT_특성"], tokenizer, model)

    # 감성 분석 결과를 데이터프레임의 새로운 열로 추가
    df[["positive_count", "negative_count", "neutral_count"]] = pd.DataFrame(sentiment_analysis_results,
                                                                             columns=["positive_count",
                                                                                      "negative_count",
                                                                                      "neutral_count"])

    # 분석 결과가 추가된 데이터프레임을 새로운 CSV 파일로 저장
    output_file_path = "gpt_sentiment_koBert.csv"
    df.to_csv(output_file_path, encoding='utf-8-sig', index=False)

    print(f"File saved at {output_file_path}")
