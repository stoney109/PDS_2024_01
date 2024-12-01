# **PDS 2024 캡스톤 디자인 I 연계 실습** 🚀

![GitHub stars](https://img.shields.io/github/stars/your-username/your-repo?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/your-username/your-repo?style=flat-square)
![License](https://img.shields.io/github/license/your-username/your-repo?style=flat-square)

## 📖 **프로젝트 개요**
유기견 입양 특성 분석을 위한 데이터 기반 접근 방법 개발

---

## 🐾 배경
유기동물 문제는 관리 비용 증가와 윤리적 딜레마를 초래  
따라서, 유기동물 문제를 해결하기 위한 가장 좋은 방법이 입양  
입양률을 높이기 위한 데이터 기반 접근이 필요

---

## 🌟 기대효과
1. **입양률 증가**: 데이터를 활용한 입양 특성 분석 및 개선.
2. **비용 절감**: 보호소 운영 효율성 증대.
3. **문제 완화**: 유기동물 문제 해결 및 윤리적 개선.
4. **데이터 기반 의사결정**: 입양 관리 시스템 구축 및 제안.

---
## ✅ **캡스톤 1 진행 상황**
1. **데이터 크롤링 완료**
   - 주요 항목: 나이(생년월일), 체중, 성별, 중성화 여부, 견종 등.
2. **데이터 전처리**
   - 생년월일 → 나이 변환.
   - 체중 정규화 및 정리.
   - 성별 및 중성화 여부 처리.
   - 견종 데이터 정리.
3. **데이터 시각화**
   - 나이 분포, 성별 비율, 견종 분포 시각화 완료.

---

## 🔄 **추가 개발 파트**
1. **데이터 크롤링 코드 개선**
   - 기존 코드를 구조화 및 최신 API 상황에 맞게 수정.

2. **데이터 전처리 코드화 및 함수화**
   - 전처리 과정을 함수화하여 코드 효율성 증대.
   - 추가 특징 데이터 전처리:
     - 텍스트 데이터 토큰화.
     - 감성 분석.

3. **시각화 개선**
   - 인사이트 중심의 시각화 방식 추가.
   - 기존 시각화 코드 함수화 및 다양한 시각화 기법 적용.

4. **분류 모델 개발**
   - 유기견 입양 특성 분류 모델 구현:
     - Decision Tree.
     - Logistic Regression.
     - K-Nearest Neighbors (K-NN).
   - 모델 성능 비교 및 최적화.

---


## 🛠 **기술 스택**
- **언어**: Python
- **라이브러리**: 
  - 데이터 처리: pandas, NumPy.
  - 시각화: Matplotlib, Seaborn,WordCloud
  - 머신러닝: Scikit-learn
  - 텍스트 처리: NLTK, spaCy


---

## 📂 **프로젝트 구조**
```plaintext
your-project/
├── src/
│   ├── main.py
│   ├── utils/
│   └── ...
├── docs/
├── tests/
├── README.md
└── ...
