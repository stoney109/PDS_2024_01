# **PDS 2024 캡스톤 디자인 I 연계 실습** 🚀

![GitHub stars](https://img.shields.io/github/stars/your-username/your-repo?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/your-username/your-repo?style=flat-square)
![License](https://img.shields.io/github/license/your-username/your-repo?style=flat-square)

## 📖 **프로젝트 개요**
유기견 입양 특성 분석

---

## 🐾 배경
유기동물 문제는 관리 비용 증가와 윤리적 딜레마를 초래  
따라서, 유기동물 문제를 해결하기 위한 가장 좋은 방법이 입양  
입양률을 높이기 위한 데이터 기반 접근이 필요

---

## 🌟 기대효과
1. 입양률 증가와 보호소 운영 비용 절감.
2. 유기동물 문제 완화 및 윤리적 개선.
3. 데이터 기반 입양 관리 시스템 제안.

---
## 캡스톤1 진행 사항
: 데이터 크롤링 완료
: 데이터 나이(생년월일),체중, 성별, 중성화 여부, 견종 전처리 완료
: 시각화 (나이,성별,견종)

---
## 추가 개발 파트
: 데이터 크롤링 부분 정리 및 현재 API 상황에 맞게 조정
: 여러부분으로 나누어져있던 전처리 방식을 코드로 정리 및 함수화하여 효율적으로 변경
: 캡스톤 1때 전처리하지 못했던 특징 부분 전처리 및 시각화
>> 토큰화, 감성분석
: 더욱 인사이트가 잘 보일 수 있도록 시각화 변경 및 코드 정리
>> 함수화 및 여러가지 방식 추가
: 여러 특성들을 활용한 분류 모델 시도
>> decision tree , logistic regression, K-nn등

---

## 🛠 **기술 스택**
- **언어**: Python
- **라이브러리**: NumPy, pandas, Matplotlib 등

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
