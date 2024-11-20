import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter


def generate_wordcloud(texts, title, font_path='C:/Windows/Fonts/malgun.ttf', background_color='white'):
    """
    주어진 텍스트 데이터를 바탕으로 워드클라우드를 생성합니다.

    :param texts: 텍스트 리스트
    :param title: 그래프 제목
    :param font_path: 워드클라우드에 사용할 폰트 경로
    :param background_color: 워드클라우드 배경색
    """
    # 텍스트 합치기
    combined_text = ' '.join(texts)

    # 단어 빈도수 계산 및 빈도수 3 이상 단어 필터링
    word_counts = Counter(combined_text.split())
    filtered_text = ' '.join([word for word, count in word_counts.items() if count > 3])

    # 워드클라우드 생성
    wordcloud = WordCloud(font_path=font_path, background_color=background_color).generate(filtered_text)

    return wordcloud


def read_csv_column(file_path, column_name, encoding='euc-kr'):
    """
    CSV 파일에서 특정 열의 데이터를 읽어옵니다.

    :param file_path: CSV 파일 경로
    :param column_name: 읽어올 열 이름
    :param encoding: CSV 파일 인코딩
    :return: 열 데이터 리스트
    """
    # 오류 발생 대비하기
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            reader = csv.DictReader(file)
            return [row[column_name] for row in reader if row[column_name].strip()]
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return []
    except KeyError:
        print(f"'{column_name}' 열을 찾을 수 없습니다.")
        return []
    except Exception as e:
        print(f"오류 발생: {e}")
        return []


if __name__ == "__main__":
    # 두 CSV 파일 경로 및 사용할 열 이름
    adopted_csv_path = '../resource/final_adopted_data.csv'  # 입양된 데이터 경로
    unadopted_csv_path = '../resource/final_unadopted_data.csv'  # 입양되지 않은 데이터 경로
    column_name = '견종'  # 분석할 열 이름

    # 두 데이터 읽기
    adopted_data = read_csv_column(adopted_csv_path, column_name)
    unadopted_data = read_csv_column(unadopted_csv_path, column_name)

    # 워드클라우드 생성
    adopted_wordcloud = generate_wordcloud(adopted_data, "Adopted_speices")
    unadopted_wordcloud = generate_wordcloud(unadopted_data, "Unadopted_speices")

    # 두 워드클라우드를 하나의 화면에 표시
    plt.figure(figsize=(16, 8))

    plt.subplot(1, 2, 1)  # 첫 번째 워드클라우드
    plt.imshow(adopted_wordcloud, interpolation='bilinear')
    plt.title("Adopted", fontsize=16)
    plt.axis('off')

    plt.subplot(1, 2, 2)  # 두 번째 워드클라우드
    plt.imshow(unadopted_wordcloud, interpolation='bilinear')
    plt.title("Unadopted", fontsize=16)
    plt.axis('off')

    plt.tight_layout()
    plt.show()
