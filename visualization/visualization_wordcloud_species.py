import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# CSV 파일에서 특정 열을 읽는 함수
def read_csv_column(file_path, column_name):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row[column_name] for row in reader]

# 워드클라우드를 생성하는 함수
def generate_wordcloud(texts, font_path='C:/Windows/Fonts/batang.ttc'):
    # 텍스트 합치기
    combined_text = ' '.join(texts)

    # 단어 빈도수 계산
    word_counts = Counter(combined_text.split())

    # 빈도수가 3 이상인 단어들로 필터링
    filtered_text = ' '.join([word for word, count in word_counts.items() if count > 3])

    # 워드클라우드 생성
    wordcloud = WordCloud(font_path=font_path, background_color='white').generate(filtered_text)
    return wordcloud

# 메인 실행 부분
if __name__ == "__main__":
    # CSV 파일 경로 및 사용할 열 이름
    adopted_csv_path = '../resource/final_adopted_data_utf8.csv'
    unadopted_csv_path = '../resource/final_unadopted_data_utf8.csv'
    column_name = '견종'

    # CSV 파일 읽기
    adopted_data = read_csv_column(adopted_csv_path, column_name)
    unadopted_data = read_csv_column(unadopted_csv_path, column_name)

    # 워드클라우드 생성
    adopted_wordcloud = generate_wordcloud(adopted_data)
    unadopted_wordcloud = generate_wordcloud(unadopted_data)

    # 두 워드클라우드를 하나의 화면에 표시
    plt.figure(figsize=(16, 8))

    # 첫 번째 워드클라우드
    plt.subplot(1, 2, 1)
    plt.imshow(adopted_wordcloud, interpolation='bilinear')
    plt.title("Adopted Species", fontsize=16)
    plt.axis('off')  # 축 제거

    # 두 번째 워드클라우드
    plt.subplot(1, 2, 2)
    plt.imshow(unadopted_wordcloud, interpolation='bilinear')
    plt.title("Unadopted Species", fontsize=16)
    plt.axis('off')  # 축 제거

    # 레이아웃 조정 및 출력
    plt.tight_layout()
    plt.show()
