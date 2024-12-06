import pandas as pd
from konlpy.tag import Okt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re


# 워드클라우드를 생성하는 함수
def generate_wordcloud(text):
    okt = Okt()  # Okt 객체 생성 (형태소 분석기)

    # 입력된 텍스트를 형태소 단위로 분리
    morphs = okt.morphs(text)

    # 특수문자 및 숫자를 제거
    morphs = [re.sub(r'[^가-힣]', '', morph) for morph in morphs]

    # 형태소들을 하나의 문자열로 결합
    joined_text = ' '.join(morphs)

    # 단어 빈도수를 계산
    word_counts = Counter(morphs)

    # 빈도수가 1 이상인 단어들만 선택하여 문자열로 결합
    joined_text = ' '.join([word for word, count in word_counts.items() if count > 3])

    # 워드클라우드 생성 (폰트 경로를 시스템의 한글 폰트로 설정)
    wordcloud = WordCloud(
        font_path='C:/Windows/Fonts/batang.ttc',  # 한글 폰트 경로
        background_color='white'  # 배경색 설정
    ).generate(joined_text)

    # 생성된 워드클라우드를 시각화
    plt.figure(figsize=(10, 5))  # 그래프 크기 설정
    plt.imshow(wordcloud, interpolation='bilinear')  # 워드클라우드 이미지를 화면에 표시
    plt.axis('off')  # 축 제거
    plt.show()  # 화면에 출력


# 메인 함수: CSV 데이터를 읽고 워드클라우드를 생성
if __name__ == "__main__":
    # CSV 파일 경로 설정
    csv_file_path = '../resource/text_preprocessing_traits/unadopted_text_cleaning_by_morphs.csv'

    # CSV 파일을 읽어 데이터프레임으로 저장
    df = pd.read_csv(csv_file_path, encoding="utf-8", low_memory=False)

    # 'Processed_Traits' 열의 데이터에서 널값(NaN)을 제외하고 가져옴
    text_column = df['Processed_Traits'].dropna()

    # 가져온 텍스트 데이터를 하나의 문자열로 결합
    combined_text = ' '.join(text_column)

    # 결합된 텍스트로 워드클라우드 생성 및 시각화
    generate_wordcloud(combined_text)

