import pandas as pd
import matplotlib.pyplot as plt
import random
import os

# 고정된 색상 매핑 생성
def generate_color_mapping(unique_labels):
    """
    고유 라벨에 고정된 색상을 생성
    :param unique_labels: list, 고유한 색상 라벨
    :return: dict, 라벨에 매핑된 고정 색상
    """
    random.seed(42)  # 시드를 고정
    color_mapping = {label: "#{:02x}{:02x}{:02x}".format(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for label in unique_labels}

    # 'other' 항목을 항상 포함하도록 조건문 설정
    if 'other' not in color_mapping:
        color_mapping['other'] = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return color_mapping

# 색상 데이터 처리 및 원 그래프 생성 함수
def process_colors_pie(data, title, ax, color_mapping):
    """
    데이터에서 색상 정보를 처리하고, 원 그래프로 시각화
    :param data: pandas DataFrame, 데이터
    :param title: str, 그래프 제목
    :param ax: matplotlib Axes, 그래프를 그릴 축
    :param color_mapping: dict, 색상 라벨에 매핑된 고정 색상
    """
    # '색상' 칼럼의 값을 소문자로 변환
    colors_lower = data['색상'].str.lower()

    # 카테고리 생성
    colors_categories = set(data['색상'].str.lower())

    # 빈도 계산 및 상위 10개 선택
    color_counts = colors_lower.value_counts()
    top_colors = color_counts.head(10)

    # '기타' 항목 추가 ( 상위 10안에 들지 못한 것들을 다 기타로 처리 )
    other_count = color_counts[10:].sum()
    if other_count > 0:
        top_colors['other'] = other_count

    # 매핑된 색상으로 컬러 설정
    colors_for_pie = [color_mapping[color] for color in top_colors.index]

    # 원 그래프 생성
    # 소수점 두자리까지 퍼센테이지 출력
    ax.pie(top_colors, labels=top_colors.index, autopct='%1.2f%%', startangle=90, colors=colors_for_pie)
    ax.set_title(title)

# 데이터 로드
adopted_csv_path = '../resource/final_adopted_data.csv'
unadopted_csv_path = '../resource/final_unadopted_data.csv'

try: # 데이터 불러오기
    adopted_data = pd.read_csv(adopted_csv_path, encoding='utf-8-sig')
    unadopted_data = pd.read_csv(unadopted_csv_path, encoding='utf-8-sig')

    # 전체 고유 라벨 추출
    unique_labels = set(adopted_data['색상'].str.lower().unique()) | set(unadopted_data['색상'].str.lower().unique())
    unique_labels.add('other')  # 'other' 항목을 명시적으로 추가

    # 고정된 색상 매핑 생성
    color_mapping = generate_color_mapping(unique_labels)

    # 그래프 생성 ( 두 그래프가 한 눈에 보이도록 생성 )
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # 입양된 데이터 원 그래프
    process_colors_pie(adopted_data, 'Adopted Top 10 Colors', axes[0], color_mapping)

    # 입양되지 않은 데이터 원 그래프
    process_colors_pie(unadopted_data, 'Unadopted Top 10 Colors', axes[1], color_mapping)

    plt.tight_layout()


    # 저장 경로 설정
    os.makedirs("visualization_png", exist_ok=True)  # 폴더 생성
    save_path = "visualization_png/piechart_color.png"

    # 그래프 저장
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"그래프가 저장되었습니다: {save_path}")

    plt.show() # 그래프 출력

except FileNotFoundError: # 파일 경로를 찾지 못할 경우
    print("CSV 파일 경로를 확인하세요.")


