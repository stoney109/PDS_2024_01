import pandas as pd
import re


def preprocess_color(dataframe):
    """
    '색상' 데이터를 전처리하는 함수

    Parameters:
        dataframe (pd.DataFrame): 전처리할 데이터프레임

    Returns:
        pd.DataFrame: 전처리된 데이터프레임
    """
    # 필요 없는 단어 및 패턴 제거
    dataframe['색상'] = dataframe['색상'].str.replace(
        r'？p|LG|APT|IC|cm|KG|Mix견|색f|도베르만|말티즈|시츄|푸들|믹스견|강아지|고등어|온순함|진도|풍산|암컷|수컷|순함|혼재|미상|조금|보라|분홍|핑크|로즈|견|빛|핵|객|섹|샛|새|\d+',
        '', regex=True)

    # '혼합' 또는 '믹스' 단일로 있는 경우 'Mix', 그렇지 않으면 제거(eg. 갈색 검정 믹스 -> 갈색 검정)
    dataframe['색상'] = dataframe['색상'].apply(
        lambda x: 'Mix' if re.fullmatch(r'(혼합|믹스)', x) else re.sub(r'(혼합|믹스)', '', x))

    # 색상 대체 딕셔너리 정의 (순서 중요)
    color_replacements = {
        '흰암|암': 'Ivory',
        'white|화이트|하얀|하양|연흰|흐니|백구|희|흰|백|벡|힌|휜|흔|힁|힄|횐|읜': 'White',
        '블루탄': 'Blue_tan',
        'Black Tan|네눈박이|연,검정|블랙탄|탄': 'Blacktan',
        '블랙마스크': 'Blackmask',
        '블루멀': 'Bluemerle',
        '연한 검정|연한검정|연한 회|짙은 회|진한 회|옅은회|연한회|짙은회|진한회|세이블|그레이|연흑|청회|진회|진,회|차콜|재구|그레|잿|쥐|회|획|재|제': 'Gray',
        'BLACK|black|블랙|검정정|검정|겅정|검은|깜장|감정|건정|까만|섬정|흑구|검|흑|블랙|블': 'Black',

        '라이트 베이지|옅은 베이지|연한 베이지|옅은베이지|여튼베이지|연한베이지|연한 노란|연한 노랑|옅은 상아|엷은노랑|연한노랑|연베이지|연브라운': 'Ivory',
        'ivory|dkdlqhfl|cream|아이보리|아아보리|아리보리|연 노랑|연노랑|연노란|크림림|오트밀|누룽지|크림크|연회|연노|크림|상아|레몬|진미|살구|살|미': 'Ivory',

        '적황|짙은 황|짙은황': 'Brown',

        '여튼브라운|연한 황토|연한 갈|옅은 갈|옅은 황|연한 황|밝은 갈|흐린 갈|여튼갈|연한황|옅은황|밝은갈|옅은갈|엷은갈|연한갈|진한갈|흐린갈|연 갈|연,갈': 'Beige',
        'Apricot|apricot|gold|베이지|배아쟈|옐로우|진노랑|오랜지|연갈|담황|인절|치즈|황생|황토|황구|황금|화운|골든|골드|연황|진황|진베|누런|누렁|노랑': 'Beige',
        'Buff|buff|노란|카키|황|항|베|노|금': 'Beige',  # 화운 확인 필요

        'brown|gmrrkftor|어두운 갈|어두운갈': 'Brown',
        '짙은 고동|진브라운|짙은 갈|진한 갈|진한갈|짙은갈|브라운|애프리|붉은갈|진,갈|진갈|찐갈|적갈|적황|흔갈|흙갈|고동|레드|붉은|진밤|초콜릿': 'Brown',

        '은갈': 'Gray',

        '진한밤|초콜렛|초코|쵸코|쪼크|커피|갈견|갈|걀|강|길|밤|적': 'Brown',

        '파티칼라|연파티|파티티|파티': 'Parti',
        '트라이칼라|세가지|트라이|삼': 'Tri',
        'BRINDLE|호랑이 무늬|호반무늬|호피무늬|호피무니|호피무뉘|브린들들|브렌드리|브랜드리|브린들|카오스|호랑|호반|호피|호구|칡': 'Brindle',
        '얼룩무늬|얼룩|얼눅|바둑|점박|젖소': 'Spotted',
        '짙은|옅은': '',
        'silver|실버|연회|은': 'Gray',
        '연': 'Ivory',
        '기타|염': 'Unknown'
    }

    # 색상 대체 패턴 적용
    for pattern, replacement in color_replacements.items():
        dataframe['색상'] = dataframe['색상'].str.replace(pattern, replacement, regex=True)

    # 영어가 아닌 값 제거 (괄호 안 포함)
    dataframe['색상'] = dataframe['색상'].apply(
        lambda x: re.sub(r'\((?![A-Za-z]+\))[^)]+\)', '', x))

    # 한글 모두 제거
    dataframe['색상'] = dataframe['색상'].str.replace('[가-힣]+', '', regex=True)

    # 문자열 좌우 공백 제거
    dataframe['색상'] = dataframe['색상'].str.strip()

    # 색상 컬럼 형태 통일 함수
    def process_color_form(color_column):
        """
        색상 컬럼을 정리하여 형태를 통일하고 중복 제거 및 알파벳 정렬하는 함수

        Parameters:
            color_column (str): 색상 컬럼의 값

        Returns:
            str: 정리된 색상 문자열
        """
        if isinstance(color_column, str):
            # 대문자를 기준으로 문자열 분리
            words = re.split('([A-Z][a-z]*)', color_column)

            # 공백을 제외하고 영어로만 이루어진 비어있지 않은 문자열만 선택
            words = [word.strip() for word in words if word.strip() and re.match('^[A-Za-z]+$', word.strip())]

            # 중복 제거 후 알파벳 정렬 (대소문자 구분 없이)
            unique_words = sorted(set(words), key=lambda x: x.lower())
            return ', '.join(unique_words).strip()
        else:
            # 입력이 문자열이 아닌 경우 기본값 반환
            return 'Unknown'

    # 추가 정리 작업: 중복 제거 및 알파벳 정렬
    dataframe['색상'] = dataframe['색상'].apply(process_color_form)

    return dataframe


# CSV 파일 경로
input_csv_file = 'preprocessing_csv_files/nonglim_birth_preprocessing.csv'
output_csv_file = 'preprocessing_csv_files/nonglim_color_preprocessing.csv'

# CSV 파일 읽기
data = pd.read_csv(input_csv_file)

# 색상 전처리 함수 수행
processed_data = preprocess_color(data)

# 최종 데이터프레임을 CSV로 저장
processed_data.to_csv(output_csv_file, encoding='utf-8-sig', index=False)

# 처리된 요소 수 출력
num_elements = len(processed_data)
print(f'처리된 데이터의 수: {num_elements}개')
