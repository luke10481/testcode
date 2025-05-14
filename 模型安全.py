from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
from torch.optim import AdamW
import os

# 加载数据集
dataset = load_dataset(r'C:\Users\59483\.cache\modelscope\hub\datasets\imdb')

# 使用正确的模型名称（推荐使用官方名称）
model_name = r'C:\Users\59483\.cache\modelscope\hub\models\evenyan\bert_tiny'

# 初始化tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize_function(examples):
    return tokenizer(
        examples['text'],
        padding='max_length',
        truncation=True,
        max_length=256,
        return_tensors='pt'
    )

# 处理数据集
tokenized_datasets = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=['text'],
    batch_size=1000
)
tokenized_datasets = tokenized_datasets.rename_column('label', 'labels')

# 设置数据格式
tokenized_datasets = tokenized_datasets.with_format(
    'torch',
    columns=['input_ids', 'attention_mask', 'labels']
)

# 划分数据集
train_dataset = tokenized_datasets['train'].shuffle(seed=42).select(range(32))
eval_dataset = tokenized_datasets['test'].shuffle(seed=42).select(range(32))

# 创建数据加载器
train_loader = DataLoader(
    train_dataset,
    batch_size=16,
    shuffle=True,
    collate_fn=lambda x: x
)

eval_loader = DataLoader(
    eval_dataset,
    batch_size=16,
    collate_fn=lambda x: x
)

# 模型定义（必须与保存的模型结构完全一致）
class TinyBERTClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=2
        )

    def forward(self, input_ids, attention_mask, labels=None):
        return self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )

# 设备设置
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
checkpoint_path = 'full_model_checkpoint.pth'

# 尝试加载已有检查点
if os.path.exists(checkpoint_path):
    # 直接加载完整模型和优化器
    checkpoint = torch.load(checkpoint_path, weights_only=False, map_location=device)
    model = checkpoint['model']
    optimizer = checkpoint['optimizer']
    start_epoch = checkpoint['epoch']
    print(f"从 epoch {start_epoch} 恢复训练")
else:
    # 初始化新模型
    model = TinyBERTClassifier().to(device)
    optimizer = AdamW(model.parameters(), lr=2e-5)
    start_epoch = 0

# 确保模型在正确的设备上
model = model.to(device)

def train():
    model.train()
    for epoch in range(start_epoch, 9):  # 总训练轮次保持3轮
        total_loss = 0
        for batch in train_loader:
            # 处理batch数据
            inputs = {
                'input_ids': torch.stack([item['input_ids'] for item in batch]).squeeze(1).to(device),
                'attention_mask': torch.stack([item['attention_mask'] for item in batch]).squeeze(1).to(device),
                'labels': torch.stack([item['labels'] for item in batch]).to(device)
            }

            optimizer.zero_grad()
            outputs = model(**inputs)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f'Epoch {epoch + 1} Loss: {total_loss / len(train_loader):.4f}')
        evaluate()

        # 保存完整模型对象
        checkpoint = {
            'epoch': epoch + 1,  # 保存下一个epoch的序号
            'model': model,
            'optimizer': optimizer,
        }
        torch.save(checkpoint, checkpoint_path)
        print(f"完整模型检查点保存于 epoch {epoch + 1}")

def evaluate():
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in eval_loader:
            inputs = {
                'input_ids': torch.stack([item['input_ids'] for item in batch]).squeeze(1).to(device),
                'attention_mask': torch.stack([item['attention_mask'] for item in batch]).squeeze(1).to(device)
            }
            labels = torch.stack([item['labels'] for item in batch]).to(device)

            outputs = model(**inputs)
            _, predicted = torch.max(outputs.logits, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f'Accuracy: {100 * correct / total:.2f}%')

train()