import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

def generate_wordcloud(texts):
    # 각 텍스트를 공백으로 합쳐서 하나의 문자열로 만듦
    combined_text = ' '.join(texts)

    # 단어 빈도수 계산
    word_counts = Counter(combined_text.split())

    # 빈도수가 1 이상인 단어들을 공백으로 합쳐서 하나의 문자열로 만듦
    joined_text = ' '.join([word for word, count in word_counts.items() if count > 1])

    wordcloud = WordCloud(font_path='C:/Windows/Fonts/batang.ttc', background_color='white').generate(joined_text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    # CSV 파일 경로 설정
    csv_file_path = 'final_adopted_data.csv'  # 실제 파일 경로로 수정

    # '세부견종' 열의 데이터 가져오기
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        text_column = [row['견종'] for row in reader]

    # 가져온 데이터로 워드클라우드 생성 및 시각화
    generate_wordcloud(text_column)
