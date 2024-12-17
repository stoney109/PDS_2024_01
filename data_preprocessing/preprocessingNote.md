# 📦 전처리 작업 문서

이 문서는 데이터셋 분석을 위해 수행된 전처리 대한 정리노트입니다.  
사용된 라이브러리, 주요 구현 세부 사항, 그리고 각 스크립트와 출력 파일의 역할이 설명되어있습니다.

---

## 📑 목차
1. 🛠 [사용된 도구 및 라이브러리](#-사용된-도구-및-라이브러리)
2. 📜 [데이터 전처리 및 분석 파일 설명](#-데이터-전처리-및-분석-파일-설명)  
   - [1. 데이터 병합 및 기본 전처리](#1-데이터-병합-및-기본-전처리)  
   - [2. 농림 데이터 전처리](#2-농림-데이터-전처리)  
   - [3. 서울 데이터 전처리](#3-서울-데이터-전처리)  
   - [4. 네이버 카페 데이터 전처리](#4-네이버-카페-데이터-전처리)  
   - [5. 입양 여부별 데이터 분리](#5-입양-여부별-데이터-분리)  
   - [6. GPT를 활용한 텍스트 전처리](#6-gpt를-활용한-텍스트-전처리)  
   - [7. Konlpy를 활용한 특징 및 종 데이터 전처리](#7-konlpy를-활용한-특징-및-종-데이터-전처리)  
   - [8. 특징 데이터 샘플링 및 정렬](#8-특징-데이터-샘플링-및-정렬)  
   - [9. 전처리를 위한 개수 확인 코드](#9-전처리를-위한-개수-확인-코드)  
   - [10. 데이터 병합](#10-데이터-병합)  
   - [11. 입양된 데이터에서 필요한 데이터 전처리](#11-입양된-데이터에서-필요한-데이터-전처리)  
   - [12. 입양 되지 않은 데이터에서 필요한 데이터 전처리](#12-입양-되지-않은-데이터에서-필요한-데이터-전처리)
3. ✨ [문서 목적](#-문서-목적)


---

## 🛠 사용된 도구 및 라이브러리

: 데이터 전처리를 위하여 사용한 라이브러리는 다음과 같습니다.

### 데이터 전처리

- **📊 Pandas**: 데이터프레임 생성 및 조작, 다양한 데이터 포맷(CSV, Excel 등) 읽기/쓰기. 대규모 데이터 정리에 필수적입니다.
- **🧮 Numpy**: 수치 데이터 연산, NaN 처리, 배열 연산의 속도를 높여주는 기능 제공.
- **🔍 Regex (re)**: 정규표현식을 활용하여 텍스트 데이터에서 패턴을 추출하거나 변환.
- **📅 datetime / timedelta**: 날짜와 시간 데이터 처리 및 계산.

### 특징 텍스트 전처리

- **🤖 OpenAI API**: GPT 기반 텍스트 전처리 및 특성 추출. 대량의 비정형 텍스트 데이터를 요약하거나 분류하는 데 활용.
- **🇰🇷 Konlpy**: 한글 자연어 처리 및 형태소 분석. 한국어 텍스트 데이터의 특성 추출 및 분석에 유용.
- **✍️ Hanspell**: 한글 맞춤법 교정. 데이터 품질 개선.

### 기타 시스템 및 병렬 처리

- **📂 OS**: 파일 및 경로 관리, 데이터 저장소 및 작업 디렉토리 관리.
- **💻 multiprocessing.Pool / cpu_count**: 병렬 처리를 통한 데이터 처리 속도 향상. 대규모 데이터 처리 작업에 효과적.
- **🌐 requests**: 웹 데이터 크롤링을 통해 API 또는 HTML 데이터를 가져오는 데 활용.
- **📝 BeautifulSoup**: HTML 파싱 및 웹 크롤링 데이터 처리.
- **⏳ TQDM**: 데이터 처리 진행 상황 시각화. 작업의 진행 상황을 실시간으로 확인 가능.
- **⚙️ subprocess**: 외부 프로세스 호출 및 명령 실행.
- **⏱️ time**: 코드 실행 시간 계산 및 대기 처리.


---

## 📜 데이터 전처리 및 분석 파일 설명

### 1. 데이터 병합 및 기본 전처리

#### `00_merge_all_data.py`

- **설명**: 다양한 출처(농림, 서울, 네이버 카페)에서 수집된 데이터를 병합하며, 중복 제거 및 공통 컬럼 정리를 수행.
- **주요 작업**:
  - 공통 컬럼(예: `이름`, `견종`, `성별` 등)만 유지하여 데이터 통합.
  - 중복 데이터 제거 및 결측값 처리.
- **출력 파일**:
  - `result_all_data.csv`: 병합된 전체 데이터셋으로, 이후 분석 및 추가 작업의 기초 데이터로 활용됨. resource 폴더에 저장.


---

### 2. 농림 데이터 전처리

#### `00_nonglim_run_preprocessing.py`

- **설명**: 농림 데이터를 단계별로 정리하여, 데이터 품질을 개선.
- **주요 작업**:
  1. **`nonglim_basic_preprocessing.py`**: 불필요한 데이터를 제거하고 주요 컬럼만 유지.
  2. **`nonglim_birth_preprocessing.py`**: 출생연도 데이터를 정규화하고, 나이를 계산.
  3. **`nonglim_color_preprocessing.py`**: 텍스트 데이터를 분석하여 색상 정보를 구조화.
  4. **`nonglim_breed_preprocessing.py`**: 견종 데이터를 세부 견종으로 분리하고, 불일치를 통일.
  5. **`nonglim_feature_preprocessing.py`**: 특징 컬럼에서 노이즈와 불필요한 데이터를 제거.
  6. **`nonglim_weight_preprocessing.py`**: 체중 데이터를 정리하고 단위를 통일.
- **출력 파일**:
  - `nonglim_weight_preprocessing.csv`: 최종 정리된 농림 데이터. 이후 통합 파일인 result_all_data.csv에 병합됨.


---

### 3. 서울 데이터 전처리

#### `00_seoul_basic_preprocessing.py`

- **설명**: 서울동물복지지원센터 크롤링 데이터를 정리하여 분석 가능하도록 전처리.
- **주요 작업**:
  - 출생연도를 `YYYY.MM` 형식으로 정리.
  - 보호 장소 데이터를 `서울특별시 + 지역명`으로 통일.
  - 견종 데이터 추출 및 세부 견종 분리하여 카테고리화.
  - 특징 컬럼에서 불필요한 텍스트 및 표현 제거.
  - 색상 데이터 추출.
  - 입양 상태를 모두 `N`로 설정 : 서울동물복지지원센터 '입양대기동물현황'의 API 데이터이므로, 모든 데이터에 입양여부를 N로 설정.
- **출력 파일**:
  - `seoul_base_preprocessing.csv`: 정리된 서울 데이터. 이후 통합 파일인 result_all_data.csv에 병합됨.


---

### 4. 네이버 카페 데이터 전처리

#### `00_cafe_basic_preprocessing.py`

- **설명**: 네이버 카페 크롤링 데이터를 정리하여 분석 가능하도록 전처리.
- **주요 작업**:
  - 텍스트 데이터 정제 : 특수문자 및 불필요한 표현 제거.
  - 크롤링 텍스트 및 제목을 통해 정보를 추출하고, `보호장소`, `견종`, `성별`, `나이`, `중성화 여부` 등의 컬럼을 새로 생성.
  - 입양 상태를 모두 `Y`로 설정 :네이버 카페의 입양완료 게시판의 크롤링 데이터 이므로, 모든 데이터에 입양여부를 Y로 설정.
  - 세부 견종 분리 및 데이터 형태 통일.
- **출력 파일**:
  - `cafe_base_preprocessing.csv`: 정리된 카페 데이터. 이후 통합 파일인 result_all_data.csv에 병합됨.


---

### 5. 입양 여부별 데이터 분리

#### `00_separate_adopted_status.py`

- **설명**: 통합 데이터(`result_all_data.csv`, `gpt_result_all_data.csv`)에서 입양 여부(`입양여부`)를 기준으로 데이터를 분리하여 추후 시각화 및 분석에 맞게 전처리.
- **출력 파일**:
  - `gpt_adopted_data.csv`, `final_adopted_data.csv`: 입양된 데이터.
  - `gpt_unadopted_data.csv`, `final_adopted_data.csv`: 입양되지 않은 데이터.


---

### 6. GPT를 활용한 텍스트 전처리

#### `trait_preprocessing/01_trait_preprocessing_with_gpt.py`

- **설명**: OpenAI GPT 3.5 turbo를 활용하여 특징 데이터를 전처리하고 주요 특성을 추출.
- **주요 작업**:
  - 성격, 건강 상태, 외모 등 주요 특성을 분석.
  - 불필요한 수식어와 중복 표현 제거.
  - 텍스트를 요약하여 간결한 데이터로 정리.
- **출력 파일**:
  - `gpt_trait_data.csv`: 총 6,280개의 데이터, GPT 기반 전처리 결과.

#### `trait_preprocessing/02_gpt_text_procesing.py`

- **설명**: GPT 전처리 데이터를 추가적으로 전처리하여 `특징` 데이터에 대한 추가 전처리 진행.
- **주요 작업**:
  - 특정 단어 및 패턴 제거.
  - 규칙 기반 매핑 및 통일 작업 수행.
  - 단일 문장으로 구성된 특징 데이터를 검증 및 최적화.
- **출력 파일**:
  - `gpt_result_all_data.csv`: 최종 정리된 GPT 특징 데이터 추가 전처리 결과. resource 폴더에 저장.


---

### 7. Konlpy를 활용한 특징 및 종 데이터 전처리

#### `trait_preprocessing/00_trait_preprocessing_with_konlpy.py`

- **설명**: Konlpy와 Hanspell을 활용한 텍스트 전처리로 데이터 품질을 높임.
- **주요 작업**:
  - 맞춤법 교정 및 불용어 제거.
  - 형태소 분석으로 명사 및 주요 단어 추출.
  - 한글 텍스트 데이터를 분석하여 자연어의 맥락을 유지하면서 간결화.
- **출력 파일**:
  - `trait_adopted_preprocessing.csv`: 입양된 데이터의 전처리 결과.
  - `trait_unadopted_preprocessing.csv`: 입양되지 않은 데이터의 전처리 결과.


---

### 8. 특징 데이터 샘플링 및 정렬

#### `trait_preprocessing/99_sorted_by_trait_length.py`

- **설명**: 특징 데이터 길이를 기준으로 정렬하여 GPT API 전처리 데이터 준비.
- **출력 파일**:
  - `sorted_result_all_data.csv`: 특징 데이터 길이 기준 정렬 결과.

#### `99_separate_for_gpt.py`

- **설명**: GPT API 호출 제한만큼의 데이터를 추출. (총 6,280개의 데이터)
- **출력 파일**:
  - `trait_preprocessing/trait_preprocessingseparate_gpt_trait_data.csv`: GPT 1차 전처리가 진행된 데이터만 추출한 결과.


---

### 9. 전처리를 위한 개수 확인 코드

#### `unique_counts` 폴더 내의 파일들

- **설명**: 데이터 전처리 이후, 다양한 컬럼에 대한 고유값의 개수를 계산하고 시각화 또는 추가 분석을 위해 정리하는 코드들이 포함되어 있습니다. 각 파일은 특정 데이터 컬럼에 대한 개수 계산 로직을 포함하고 있습니다.
- **출력 형식**:
  - `adopted_status_counts.py`: 입양여부 데이터,
  - `breed_counts.py`: 견종 데이터,
  - `color_counts.py`: 색상 데이터,
  - `detail_breed_counts.py`: 세부 견종 데이터,
  - `neutral_counts.py`: 중성화 여부 전처리 결과에서 고유값을 추출하고 빈도를 계산하여 개수를 출력.
  - `trait_gpt_counts.py` : GPT 전처리 결과에서 고유값을 추출하고 빈도를 계산하여 csv 결과로 이를 저장(trait_preprocessing 폴더).

---

### 10. 데이터 병합

#### `merge_version1_data.py` / `merge_version2_data.py`

- **설명**: 학습 데이터와 테스트 데이터를 병합하여 분석에 필요한 통합 데이터를 생성.
- **주요 작업**:
  - `merge_version1_data.py`: `adopted_data_for_dt_version1.csv`와 `unadopted_data_for_dt_version1.csv` 병합.
  - `merge_version2_data.py`: `adopted_data_for_dt_version2.csv` 와 `unadopted_data_for_dt_version2.csv`를 병합.
- **출력 파일**:
  - `merged_data_version1.csv`: 버전 1 데이터 병합 결과.
  - `merged_data_version2.csv`: 버전 2 데이터 병합 결과.

---

### 11. 입양된 데이터에서 필요한 데이터 전처리

#### `adopted_data_for_decision_tree_version1.py` / `adopted_data_for_decision_tree_version2.py`

- **설명**: 학습 데이터를 위해 입양된 데이터에서 샘플을 추출하고 전처리.
- **주요 작업**:
  - `adopted_data_for_decision_tree_version1.py`:
    - 입양된 데이터에서 10,000건의 샘플을 무작위로 추출.
    - 견종, 나이, 체중, 성별, 중성화 여부를 수치형으로 전처리:
      - 견종: 믹스(0), 기타(1).
      - 나이: 소수점 앞자리만 유지.
      - 체중: 반올림.
      - 성별: M(0), F(1), Q(2).
      - 중성화 여부: Y(0), N(1), U(2).
  - `adopted_data_for_decision_tree_version2.py`:
    - 동일한 샘플링 방식으로 데이터 추출.
    - Q 및 U 값을 가진 데이터를 제외.
    - 나이와 체중의 소수점 첫째 자릿수 유지
      - 성별: M(0), F(1).
      - 중성화 여부: Y(0), N(1).
- **출력 파일**:
  - `adopted_data_for_dt_version1.csv`: 버전 1 데이터 전처리 결과.
  - `adopted_data_for_dt_version2.csv`: 버전 2 데이터 전처리 결과.

---

### 12. 입양 되지 않은 데이터에서 필요한 데이터 전처리 

#### `unadopted_data_for_decision_tree_version1.py` / `unadopted_data_for_decision_tree_version2.py`

- **설명**: 테스트 데이터를 위해 입양되지 않은 데이터에서 샘플을 추출하고 전처리.
- **주요 작업**:
  - `unadopted_data_for_decision_tree_version1.py`:
    - 입양되지 않은 데이터에서 10,000건의 샘플을 무작위로 추출.
    - 견종, 나이, 체중, 성별, 중성화 여부를 수치형으로 전처리:
      - 견종: 믹스(0), 기타(1).
      - 나이: 소수점 앞자리만 유지.
      - 체중: 반올림.
      - 성별: M(0), F(1), Q(2).
      - 중성화 여부: Y(0), N(1), U(2).
  - `undopted_data_for_decision_tree_version1.py`:
    - 동일한 샘플링 방식으로 데이터 추출.
    - Q 및 U 값을 가진 데이터를 제외.
    - - 나이와 체중의 소수점 첫째 자릿수 유지
      - 성별: M(0), F(1).
      - 중성화 여부: Y(0), N(1).
- **출력 파일**:
  - `unadopted_data_for_dt_version1.csv`: 버전 1 데이터 전처리 결과.
  - `unadopted_data_for_dt_version2.csv`: 버전 2 데이터 전처리 결과

---

## ✨ 문서 목적

**각 스크립트의 역할 및 데이터 흐름을 명확히 설명하여 작업 전반의 이해를 돕기 위해 작성되었습니다.**
