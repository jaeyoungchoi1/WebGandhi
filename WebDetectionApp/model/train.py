# 필요한 라이브러리 설치
!pip install transformers --upgrade
!pip install torch
!pip install pandas
!pip install scikit-learn

# 라이브러리 임포트
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer, AdamW, get_linear_schedule_with_warmup
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import numpy as np


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 데이터셋 로드
df = pd.read_csv('/content/drive/My Drive/comments_with_profanity.csv')
comments = df['Comment'].values
labels = df['Class'].values

# 토크나이저 로드
tokenizer = DistilBertTokenizer.from_pretrained('monologg/distilkobert')

# 데이터셋 클래스 정의
class CommentsDataset(Dataset):
    def __init__(self, comments, labels, tokenizer, max_len=128):
        self.comments = comments
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.comments)

    def __getitem__(self, idx):
        comment = str(self.comments[idx])
        label = self.labels[idx]

        encoding = self.tokenizer.encode_plus(
            comment,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
            truncation=True,
        )

        return {
            'comment_text': comment,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# 데이터셋 분할
train_comments, val_comments, train_labels, val_labels = train_test_split(comments, labels, test_size=0.1, random_state=42)

# 데이터 로더 생성
train_dataset = CommentsDataset(train_comments, train_labels, tokenizer)
val_dataset = CommentsDataset(val_comments, val_labels, tokenizer)
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)

# 모델 로드

epochs = 50
model = DistilBertForSequenceClassification.from_pretrained('monologg/distilkobert', num_labels=2)
model.to(device)
optimizer = AdamW(model.parameters(), lr=5e-5)  # 학습률 변경
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=len(train_loader) * epochs)

