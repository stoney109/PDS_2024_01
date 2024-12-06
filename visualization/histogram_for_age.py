import matplotlib.pyplot as plt
import pandas as pd
##TODO : 나이 컬럼 생성후 한번 더 오류 안나는 지 확인 필요
def plot_age_histogram(adopted_data, unadopted_data):
    """
    입양된 데이터와 입양되지 않은 데이터의 '나이'를 비율 기반 히스토그램으로 시각화

    :param adopted_data: pandas DataFrame, 입양된 데이터
    :param unadopted_data: pandas DataFrame, 입양되지 않은 데이터
    """
    # '나이' 데이터를 숫자로 변환 (문자형 데이터 제거 및 NaN 처리)
    if '나이' not in adopted_data.columns or '나이' not in unadopted_data.columns:
        print("데이터에 '나이' 컬럼이 없습니다. 데이터를 확인하세요.")
        return

    adopted_data['나이'] = pd.to_numeric(adopted_data['나이'], errors='coerce')
    unadopted_data['나이'] = pd.to_numeric(unadopted_data['나이'], errors='coerce')

    # 데이터 정리 (0 이상 10 이하로 필터링 - 아웃라이어 제거)
    adopted_age = adopted_data[(adopted_data['나이'] >= 0) & (adopted_data['나이'] <= 10)]['나이']
    unadopted_age = unadopted_data[(unadopted_data['나이'] >= 0) & (unadopted_data['나이'] <= 10)]['나이']

    # 필터링된 데이터 확인
    if adopted_age.empty:
        print("필터링 후 '입양된 데이터'에 나이 정보가 없습니다.")
        return
    if unadopted_age.empty:
        print("필터링 후 '입양되지 않은 데이터'에 나이 정보가 없습니다.")
        return

    # 히스토그램 생성
    fig, ax = plt.subplots(figsize=(10, 6))

    # 두 그룹의 나이 히스토그램 (비율 기반)
    bins = 20  # 히스토그램의 구간 수
    ax.hist(
        adopted_age,
        bins=bins,
        alpha=0.7,  # 투명도
        density=True,  # 비율로 변환
        label='Adopted',
        color='blue',
        edgecolor='black',
    )
    ax.hist(
        unadopted_age,
        bins=bins,
        alpha=0.7,
        density=True,
        label='Unadopted',
        color='green',
        edgecolor='black',
    )

    # 레이블 및 제목 설정
    ax.set_xlabel('Age')  # X축 레이블
    ax.set_ylabel('Proportion')  # Y축 레이블
    ax.set_title('Proportional Histogram of Adopted and Unadopted Ages')  # 제목
    ax.legend()  # 범례 추가

    plt.tight_layout()  # 레이아웃 조정
    plt.show()  # 그래프 출력


# CSV 파일 경로 설정
adopted_csv_path = '../resource/final_adopted_data.csv'  # 입양된 데이터 경로
unadopted_csv_path = '../resource/final_unadopted_data.csv'  # 입양되지 않은 데이터 경로

# 데이터 읽기 및 시각화 호출
try:
    adopted_data = pd.read_csv(adopted_csv_path, encoding='utf-8-sig', low_memory=False)  # 입양된 데이터
    unadopted_data = pd.read_csv(unadopted_csv_path, encoding='utf-8-sig', low_memory=False)  # 입양되지 않은 데이터

    plot_age_histogram(adopted_data, unadopted_data)  # 히스토그램 생성 및 출력

except FileNotFoundError: # 파일을 찾을 수 없는 경우에
    print("파일을 찾을 수 없습니다. 경로를 확인하세요.")

