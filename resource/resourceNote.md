# 💾 리소스 폴더 문서  

이 문서는 리소스 폴더 내에 저장된 각 파일에 대한 정리노트입니다.

---

## 📜 데이터 파일 설명

: crawling_data 폴더 내의 `_2024.csv` 파일을 제외하고 모든 데이터들은 **2023년 11월 16일 기준** 데이터임을 명시합니다.



### 📂 **resource** 폴더
1. **result_all_data.csv**

   : 각 크롤링 데이터에서 '특징' 열에 대한 추가 전처리를 제외한 전처리가 완료된 파일의 **전체 병합 파일**로, 약 24만개의 데이터가 포함되어있습니다.
2. **final_adopted_data.csv**

   : 위 데이터에서 입양여부가  **Y**인 데이터입니다.
3. **final_unadopted_data.csv**

   : 위 데이터에서 입양여부가  **N**인 데이터입니다.

---

### 🕸️ **crawling_data** 폴더
1. **cafe_crawling_adopted_2024.csv**, **cafe_crawling_unadopted_2024.csv**

   : 서울동물복지 지원센터의 네이버 카페 데이터 크롤링 **2024년도 신규 기준** 데이터로 각각 입양여부가 Y(adopted)인 경우와 N(unadopted)인 경우로 나눠진 데이터입니다.
3. **cafe_crawling_20231116.csv**

   : 서울동물복지 지원센터의 네이버 카페 데이터 크롤링 **2023년 11월 16일 기준** 데이터입니다.
4. **nonglim_crawling_2024.csv**

   : 농림축산검역본부 국가동물보호정보시스템 구조동물 조회 서비스 API 크롤링 **2024년도 신규 기준** 데이터입니다.
5. **nonglim_crawling_20231116.csv**

   : 농림축산검역본부 국가동물보호정보시스템 구조동물 조회 서비스 API 크롤링 **2023년 11월 16일 기준** 데이터입니다.
6. **seoul_crawling_2024.csv**

   : 서울동물복지지원센터 데이터 API 크롤링 **2024년도 신규 기준** 데이터입니다.
7. **seoul_crawling_20231116.csv**

   : 서울동물복지지원센터 데이터 API 크롤링 **2023년 11월 16일 기준** 데이터입니다.
  
---

### 🌳 **decision_tree_preprocessed_data** 폴더
1. **merged_version1.csv / merged_version2.csv**

   : 입양 된 데이터와 입양되지 않은 데이터를 합한 총 데이터입니다.

2. **adopted_data_for_dt_version1.csv / adopted_data_for_dt_version2.csv **

   : 입양 된 데이터에서 decision tree를 위한 전처리를 수행한 데이터입니다.

3. **unadopted_data_for_dt_version1.csv / unadopted_dat_for_dt_version2.csv**

   : 입양 되지 않은 데이터에서 decision tree를 위한 전처리를 수행한 데이터입니다.

---

### 🤖 **gpt_preprocessed_data** 폴더
1. **gpt_result_all_data.csv**

   : GPT 3.5 turbo API를 활용하여 RPD 제한 데이터 개수 **총 6,280개**의 '특징' 텍스트 데이터 전처리 결과가 포함된 파일입니다.
2. **gpt_adopted_data.csv**

   : 위 데이터에서 입양여부가  **Y**인 데이터입니다.
3. **gpt_unadopted_data.csv**

   : 위 데이터에서 입양여부가  **N**인 데이터입니다.

---

### 🇰🇷 **trait_preprocessed_data** 폴더
1. **trait_adopted_preprocessing.csv**

   : Konlpy와 Hanspell을 활용한 **약 24만개**의 '특징' 텍스트 데이터 전처리 결과가 포함된 파일입니다.
   : 입양여부가  **Y**인 데이터입니다.
2. **trait_unadopted_preprocessing.csv**

   : 위 데이터에서 입양여부가  **N**인 데이터입니다.

---

## ✨ 문서 목적

**각 리소스 파일의 데이터 정의를 명확히 설명하여 작업 전반의 이해를 돕기 위해 작성되었습니다.**
