import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

#워드클라우드를 사용하기 위한 함수
def generate_wordcloud(texts):
    # 각 텍스트를 공백으로 합쳐서 하나의 문자열로 만듦
    combined_text = ' '.join(texts)

    # 단어 빈도수 계산
    word_counts = Counter(combined_text.split())

    # 빈도수가 1 이상인 단어들을 공백으로 합쳐서 하나의 문자열로 만듦
    joined_text = ' '.join([word for word, count in word_counts.items() if count > 1])

    #워드클라우드 기본 설정
    wordcloud = WordCloud(font_path='C:/Windows/Fonts/batang.ttc', background_color='white').generate(joined_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

##실제 코드 실행 부분
#파일 읽어오기
csv_file_path = '../resource/final_adopted_data.csv'
file = open(csv_file_path, 'r')
#파일 안의 컬럼 가져오고 파일 닫기
reader = csv.DictReader(file)
text_column = [row['견종'] for row in reader]
file.close()

#워드클라우드 실행하기
generate_wordcloud(text_column)