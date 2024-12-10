from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

# 데이터 로드
data_path = "../resource/output_with_sentiment.csv"
dataset = load_dataset("csv", data_files={"train": data_path})

# 토크나이저 로드
model_name = "monologg/koelectra-base-v3-discriminator"  # 사용할 사전 학습 모델
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 데이터 전처리 함수
def preprocess_function(examples):
    return tokenizer(examples["GPT_특성"], truncation=True, padding=True, max_length=128)

# 데이터 전처리
tokenized_datasets = dataset.map(preprocess_function, batched=True)

# 모델 로드
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)  # 3개의 라벨: 긍정, 부정, 중립

# 학습 설정
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
)

# Trainer 생성
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
)

# Fine-Tuning 수행
trainer.train()

# 모델 저장
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")

print("Fine-Tuning 완료! 모델이 './fine_tuned_model'에 저장되었습니다.")
