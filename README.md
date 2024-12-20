# **PDS 2024 캡스톤 디자인 I 연계 실습** 🚀

## 👩‍🦰 **참여자**
2021111691 배나현  
2023111774 공다원  
2023111777 김수지  
2023111802 윤서현  



## 📖 **프로젝트 개요**  
**데이터 분석과 머신러닝 기술을 활용하여 유기견 입양률 향상을 위한 전략적 방향성 제시**

---

## 🐾 **배경**  
- 유기동물 문제는 단순히 윤리적 딜레마를 넘어, 사회적 비용과 자원 낭비를 초래하는 복합적인 이슈입니다.  
- 입양률을 높이고 유기동물 보호 체계의 효율성을 강화하기 위해서는 데이터를 기반으로 한 심층적인 분석과 예측 모델이 필요합니다.  
- 본 프로젝트는 데이터 크롤링, 전처리, 분석, 시각화, 그리고 머신러닝 기반 모델링을 통해 입양 특성에 대한 인사이트를 도출하고, 향후 효율적인 솔루션 개발을 위한 기반을 마련하는 것을 목표로 합니다. 

---

## 🌟 기대효과
1. **입양률 증가**: 데이터를 활용한 입양 특성 분석으로 입양률 개선.  
2. **비용 절감**: 보호소 운영 효율성 증대.  
3. **문제 완화**: 유기동물 문제 해결 및 윤리적 개선.  
4. **데이터 기반 의사결정**: 입양 관리 시스템 구축 및 제안.  

---

## ✅ **캡스톤 I 진행 상황**
1. **데이터 크롤링 완료**
   - 주요 항목: 나이, 체중, 성별, 중성화 여부, 견종 등.

2. **데이터 전처리**
   - 생년월일 → 나이 변환.
   - 체중 정규화 및 정리.
   - 성별 및 중성화 여부 처리.
   - 견종 데이터 정리.

3. **데이터 시각화**
   - 나이 분포, 성별 비율, 견종 분포 시각화 완료.

---

## 🔄 **추가 개발 및 개선 내용**
1. **크롤링 코드 개선**
> ver. 2024 data
   - 크롤링 과정 자동화 및 병렬 처리 적용.
   - 최신 API와 웹사이트 구조 변경에 따른 업데이트.

  
2. **데이터 전처리 코드 최적화**
> ver. 2023 data
   - 크롤링 데이터 병합 및 중복 제거 과정 최적화.
   - 전처리 과정을 함수화하여 코드 효율성 증대.
   - 추가 특징 데이터 전처리 (예: 텍스트 데이터 토큰화).
      - GPT API를 활용한 텍스트 정제와 특성 추출.
      - Konlpy와 Hanspell을 사용해 한국어 텍스트의 품질 개선.
  

3. **시각화 개선**
> ver. 2023 data
   - 인사이트 중심의 시각화 방식 추가.
   - 기존 시각화 코드 함수화 및 다양한 시각화 기법 적용.
      - 막대 그래프: 성별과 중성화 상태의 분포를 누적 막대 그래프로 표시.
      - 히스토그램: 나이와 체중의 빈도 분포를 통해 주요 범위 분석.
      - 원형 차트: 색상 데이터의 비율 시각화.
      - 워드 클라우드: 특징 데이터 및 종(species) 데이터를 활용한 단어 빈도 시각화.
  

4. **모델 구현**
> ver. 2023 data
   - 감성 분석 모델 활용 (koBERT): 긍정, 부정, 중립 감정을 분석.
   - 유기견 입양 특성 분류 모델 구현 (Decision Tree): 입양 여부를 target으로 활용. 두 가지 데이터셋(Version 1, Version 2)으로 성능 비교. 어떤 컬럼이 주요하게 작용하는지 파악.

---

## 🛠 **기술 스택**

### 🚀 데이터 크롤링
- **pandas**: 데이터 분석 및 처리.
- **selenium**: 웹 브라우저 자동화.
- **BeautifulSoup**: HTML 파싱 및 데이터 처리.
- **requests**: HTTP 요청 및 API 데이터 가져오기.
- **re**: 문자열 검색 및 수정.
- **concurrent.futures**: 병렬 작업을 위한 스레드 풀 생성.

### 🔧 데이터 전처리
- **pandas**: 데이터 분석 및 처리.
- **numpy**: 수치 연산과 데이터 처리.
- **Konlpy(Okt)**: 한글 텍스트 형태소 분석 및 전처리.
- **Hanspell**: 한글 맞춤법 검사 및 교정.
- **re**: 정규표현식을 사용한 텍스트 전처리.
- **tqdm**: 코드 진행 상황 Progress Bar.
- **multiprocessing**: 병렬 처리 및 CPU 최적화.
- **datetime**: 날짜와 시간 데이터 처리.
- **OpenAI API**: GPT 기반 데이터 전처리.
- **subprocess**: 외부 프로세스 호출 및 명령 실행.

### 📈 데이터 시각화
- **pandas**: 데이터 분석 및 처리.
- **matplotlib**: 막대 그래프, 히스토그램, 원형 차트 생성.
- **wordCloud**: 텍스트 데이터를 기반으로 워드 클라우드 생성.
- **random**: 시각화 색상 결정 등 무작위 데이터 생성.
- **csv**: CSV 파일 읽기 및 쓰기.
- **collections.Counter**: 데이터 카운트 및 빈도 계산.

### 🧠 모델 학습 
- **pandas**: 데이터 분석 및 처리.
- **sklearn**: Decision Tree 모델 생성 및 성능 지표 계산.
- **transformers**: 자연어 처리 모델 활용 (koBERT).
- **torch**: PyTorch를 사용한 딥러닝 계산.

---

## 📂 **프로젝트 구조**
- **data_crawling**  
  ➡️ Naver Cafe, 농림 API, 서울복지지원센터 API 크롤링 코드.
  ([crawlingNote](https://github.com/stoney109/PDS_2024_01/blob/main/data_crawling/crawlingNote.md))

- **data_preprocessing**  
  ➡️ 결측값 처리, 데이터 정제 및 전처리 코드.
  ([preprocessingNote](https://github.com/stoney109/PDS_2024_01/blob/main/data_preprocessing/preprocessingNote.md))

- **visualization**  
  ➡️ 데이터 시각화 스크립트 및 결과.
  ([visualizationNote](https://github.com/stoney109/PDS_2024_01/blob/main/visualization/visualizationNote.md))

- **models**  
  ➡️ Decision Tree 모델 학습 및 결과와 koBERT 사전 학습 모델 사용 결과 저장.
  ([modelsNote](https://github.com/stoney109/PDS_2024_01/blob/main/models/modelsNote.md))

- **resource**  
  ➡️ 프로젝트 데이터셋 및 리소스.
  ([resourceNote](https://github.com/stoney109/PDS_2024_01/blob/main/resource/resourceNote.md))




---

