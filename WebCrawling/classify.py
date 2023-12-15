!pip install transformers
!pip install datasets==1.17.0
!pip install transformers -U
!pip install torch -U
!pip install accelerate -U
from google.colab import drive
drive.mount('/content/drive')
from datasets import load_dataset
from datasets import Dataset
import pandas as pd
from transformers import AutoTokenizer
from sklearn.metrics import label_ranking_average_precision_score
from sklearn.model_selection import train_test_split
# 데이터셋 로드
df = pd.read_csv('/content/drive/My Drive/comments_with_profanity.csv')
df.rename(columns={'Comment': '문장', 'Class': '욕설'}, inplace=True)
# 훈련 데이터와 검증 데이터로 분리
train_df, valid_df = train_test_split(df, test_size=0.1)

# Hugging Face Dataset 형식으로 변환
train_dataset = Dataset.from_pandas(train_df)
valid_dataset = Dataset.from_pandas(valid_df)
# Transformers tokenizer 초기화
model_name = 'beomi/kcbert-base'
tokenizer = AutoTokenizer.from_pretrained(model_name)
# 데이터셋 전처리 함수
def preprocess_function(examples):
    tokenized_examples = tokenizer(str(examples["문장"]))
    # 레이블을 Float 타입으로 변환
    tokenized_examples['labels'] = float(examples['욕설'])
    return tokenized_examples
  # 데이터셋을 Hugging Face Dataset 형식으로 변환
  tokenized_train_dataset = train_dataset.map(preprocess_function)
  tokenized_train_dataset.set_format(type='torch', columns=['input_ids', 'labels', 'attention_mask', 'token_type_ids'])
  tokenized_eval_dataset = valid_dataset.map(preprocess_function)
  tokenized_eval_dataset.set_format(type='torch', columns=['input_ids', 'labels', 'attention_mask', 'token_type_ids'])
tokenized_train_dataset[0]
from transformers import BertForSequenceClassification, TrainingArguments, Trainer, DataCollatorWithPadding
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
model = BertForSequenceClassification.from_pretrained(
  model_name,
  num_labels=1,  # 이진 분류 문제에 맞춰 설정
)

# 이진 분류 레이블
model.config.id2label = {0: 'neutral', 1: 'hate'}
model.config.label2id = {'neutral': 0, 'hate': 1}
model.config.label2id
from sklearn.metrics import label_ranking_average_precision_score
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np
def compute_metrics(pred):
labels = pred.label_ids
preds = pred.predictions[:, 0]  # 이진 분류에서는 첫 번째 열이 예측값입니다.
preds = np.where(preds > 0.0, 1, 0)  # 예측값을 이진화합니다.

precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
acc = accuracy_score(labels, preds)
return {
    'accuracy': acc,
    'f1': f1,
    'precision': precision,
    'recall': recall
}
# 훈련 설정
training_args = TrainingArguments(
    output_dir="/content/drive/My Drive/12_15_model_output",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    num_train_epochs=5,
    save_strategy='epoch',
    load_best_model_at_end=True,
    metric_for_best_model='f1',
    greater_is_better=True,
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_eval_dataset,
    compute_metrics=compute_metrics,
    tokenizer=tokenizer,
    data_collator=data_collator
)
trainer.train()
trainer.save_model()