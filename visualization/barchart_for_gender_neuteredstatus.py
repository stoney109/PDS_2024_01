import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_bar_charts_percentage_with_labels(adopted_data, unadopted_data):
    """
    입양된 데이터와 입양되지 않은 데이터를 성별 및 중성화 여부로 나누어 비율 기반 막대그래프로 시각화하며, 그래프 위에 비율 표시를 추가합니다.

    :param adopted_data: pandas DataFrame, 입양된 데이터
    :param unadopted_data: pandas DataFrame, 입양되지 않은 데이터
    """
    # 데이터 그룹화: 성별과 중성화 여부로 그룹화하여 빈도 계산
    adopted_grouped = adopted_data.groupby(['성별', '중성화 여부']).size().unstack(fill_value=0)
    unadopted_grouped = unadopted_data.groupby(['성별', '중성화 여부']).size().unstack(fill_value=0)

    # 비율 계산
    adopted_percentage = adopted_grouped.div(adopted_grouped.sum(axis=1), axis=0) * 100
    unadopted_percentage = unadopted_grouped.div(unadopted_grouped.sum(axis=1), axis=0) * 100

    # 막대그래프 그리기
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))  # 1행 2열 그래프 설정

    # 입양된 데이터 막대그래프
    ax1 = adopted_percentage.plot(
        kind='bar',
        stacked=True,
        colormap='Pastel1',
        edgecolor='black',
        ax=axes[0]
    )
    axes[0].set_title('Adopted: Gender and Neutering Status (%)', fontsize=14)  # 그래프 제목
    axes[0].set_xlabel('Gender', fontsize=12)  # X축 레이블
    axes[0].set_ylabel('Percentage (%)', fontsize=12)  # Y축 레이블
    axes[0].legend(title='Neutering Status', fontsize=10, loc='upper right')  # 범례

    # 각 막대 위에 비율(%) 표시
    for p in ax1.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        if height > 0:  # 0%인 막대는 표시하지 않음
            axes[0].text(
                x + width / 2,
                y + height / 2,
                f'{height:.1f}%',
                ha='center',
                va='center',
                fontsize=9
            )

    # 입양되지 않은 데이터 막대그래프
    ax2 = unadopted_percentage.plot(
        kind='bar',
        stacked=True,
        colormap='Set3',
        edgecolor='black',
        ax=axes[1]
    )
    axes[1].set_title('Not Adopted: Gender and Neutering Status (%)', fontsize=14)  # 그래프 제목
    axes[1].set_xlabel('Gender', fontsize=12)  # X축 레이블
    axes[1].set_ylabel('Percentage (%)', fontsize=12)  # Y축 레이블
    axes[1].legend(title='Neutering Status', fontsize=10, loc='upper right')  # 범례

    # 각 막대 위에 비율(%) 표시
    for p in ax2.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        if height > 0:  # 0%인 막대는 표시하지 않음
            axes[1].text(
                x + width / 2,
                y + height / 2,
                f'{height:.1f}%',
                ha='center',
                va='center',
                fontsize=9
            )

    # 레이아웃 조정 및 그래프 출력
    plt.tight_layout()
    plt.show()

    # 저장 경로 설정
    os.makedirs("visualization_png", exist_ok=True)  # 폴더가 없으면 생성
    save_path = "visualization_png/barchart_gender_neutering.png"

    # 그래프 저장
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"그래프가 저장되었습니다: {save_path}")


# CSV 파일 경로 설정
adopted_csv_path = '../resource/final_adopted_data.csv'  # 입양된 데이터 경로
unadopted_csv_path = '../resource/final_unadopted_data.csv'  # 입양되지 않은 데이터 경로

# 데이터 읽기 및 함수 호출
try:
    # CSV 파일 읽기
    adopted_data = pd.read_csv(adopted_csv_path, encoding='utf-8-sig', low_memory=False)  # 입양된 데이터
    unadopted_data = pd.read_csv(unadopted_csv_path, encoding='utf-8-sig', low_memory=False)  # 입양되지 않은 데이터

    # 비율 기반 막대그래프 시각화 함수 호출 (그래프 위에 비율 표시 포함)
    plot_bar_charts_percentage_with_labels(adopted_data, unadopted_data)

except FileNotFoundError as e:  # 파일 경로가 잘못되었을 경우 처리
    print(f"파일을 찾을 수 없습니다: {e}")
