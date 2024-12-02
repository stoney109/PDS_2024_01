import subprocess


'''
◆ 농림축산식품부 API 데이터 전처리 코드를 한 번에 실행하는 파일입니다.
'''


# 농림축산식품부 API 데이터를 전처리하기 위한 단계별 스크립트 파일 경로
scripts = [
    "nonglim_basic_preprocessing.py",        # 1단계: 기본 전처리
    "nonglim_birth_preprocessing.py",        # 2단계: '출생연도' 전처리
    "nonglim_color_preprocessing.py",        # 3단계: '색상' 전처리
    "nonglim_breed_preprocessing.py",        # 4단계: '견종' 전처리
    "nonglim_feature_preprocessing.py",      # 5단계: '특징' 전처리
    "nonglim_weight_preprocessing.py"        # 6단계: '체중' 전처리
]


# 각 스크립트를 순차적으로 실행 (try-except 예외처리)
for script in scripts:
    try:
        # 현재 실행 중인 스크립트 출력
        print(f"실행 중: {script}")
        # 스크립트 실행
        subprocess.run(["python", script], check=True)
        # 스크립트 실행 완료 메시지 출력
        print(f"완료: {script}\n")
    except subprocess.CalledProcessError as e:
        # 스크립트 실행 중 오류가 발생한 경우 에러 메시지 출력
        print(f"Error occurred while running {script}: {e}")
        # 오류 발생 시 루프 종료
        break


# 모든 전처리 단계 완료 메시지 출력
print("◆ 농림축산식품부 API 데이터의 모든 전처리 단계가 완료되었습니다 ◆")
