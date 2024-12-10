import matplotlib.pyplot as plt
import pandas as pd
import os


def plot_weight_histogram(adopted_data, unadopted_data):
    """
    입양된 데이터와 입양되지 않은 데이터의 '체중'을 비율 기반 히스토그램으로 시각화

    :param adopted_data: pandas DataFrame, 입양된 데이터
    :param unadopted_data: pandas DataFrame, 입양되지 않은 데이터
    """
    # '체중' 데이터를 숫자로 변환 (문자형 데이터 제거 및 NaN 처리)
    adopted_data['체중'] = pd.to_numeric(adopted_data['체중'], errors='coerce')
    unadopted_data['체중'] = pd.to_numeric(unadopted_data['체중'], errors='coerce')

    # 데이터 정리 (20 이하로 필터링 - 아웃라이어들 제거)
    adopted_weight = adopted_data[adopted_data['체중'] <= 20]['체중']
    unadopted_weight = unadopted_data[unadopted_data['체중'] <= 20]['체중']

    # 히스토그램 생성
    fig, ax = plt.subplots(figsize=(10, 6))

    # 두 그룹의 체중 히스토그램 (비율 기반)
    bins = 20  # 히스토그램의 구간 수
    ax.hist(
        adopted_weight,
        bins=bins, # 히스토그램의 구간 수
        alpha=0.7, # 투명도
        density=True,  # density=True: 빈도를 전체 데이터의 비율로 변환
        label='Adopted',
        color='blue',
        edgecolor='black',
    )
    ax.hist(
        unadopted_weight,
        bins=bins, # 히스토그램의 구간 수
        alpha=0.7, # 투명도
        density=True,  # density=True: 빈도를 전체 데이터의 비율로 변환
        label='Unadopted',
        color='green',
        edgecolor='black',
    )

    # 레이블 및 제목 설정
    ax.set_xlabel('Weight') # X축 레이블: 체중
    ax.set_ylabel('Proportion') # Y축 레이블: 전체 비율
    ax.set_title('Proportional Histogram of Adopted and Unadopted Weights') # 그래프 제목
    ax.legend()

    plt.tight_layout() # 레이아웃 자동 조정
    plt.show() # 그래프 출력

    # 저장 경로 설정
    os.makedirs("visualization_png", exist_ok=True)  # 폴더가 없으면 생성
    save_path = "visualization_png/histogram_weight.png"

    # 히스토그램 저장
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"히스토그램이 저장되었습니다: {save_path}")


# 두 CSV 파일 경로
adopted_csv_path = '../resource/final_adopted_data.csv'  # 입양된 데이터 경로
unadopted_csv_path = '../resource/final_unadopted_data.csv'  # 입양되지 않은 데이터 경로

# 데이터 읽기
try:
    # low_memory=False : 메모리 사용을 최적화하면서 경고를 방지
    adopted_data = pd.read_csv(adopted_csv_path, encoding='utf-8-sig', low_memory=False)  # 입양된 데이터
    unadopted_data = pd.read_csv(unadopted_csv_path, encoding='utf-8-sig', low_memory=False)  # 입양되지 않은 데이터

except FileNotFoundError: # 파일이 없을 경우 에러 처리
    print("파일을 찾을 수 없습니다. 경로를 확인하세요.")
    exit()

# 히스토그램 시각화 호출
plot_weight_histogram(adopted_data, unadopted_data)

