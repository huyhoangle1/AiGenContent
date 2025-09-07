from transformers import GPT2Tokenizer, GPT2LMHeadModel, TrainingArguments, Trainer
import torch
import pandas as pd
import os

class ContentDataset(torch.utils.data.Dataset):
    def __init__(self, texts, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.inputs = tokenizer(
            texts,
            max_length=max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
    
    def __len__(self):
        return len(self.inputs["input_ids"])
    
    def __getitem__(self, idx):
        return {
            "input_ids": self.inputs["input_ids"][idx],
            "attention_mask": self.inputs["attention_mask"][idx],
            "labels": self.inputs["input_ids"][idx]
        }

def train_model():
    # Tải dữ liệu đã xử lý
    train_data = pd.read_csv("data/processed/train_data.csv")
    train_texts = train_data["clean_text"].tolist()
    
    # Tải tokenizer và mô hình
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token
    
    # Tạo dataset
    train_dataset = ContentDataset(train_texts, tokenizer)
    
    # Thiết lập tham số huấn luyện
    training_args = TrainingArguments(
        output_dir="./models/checkpoints",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=10_000,
        save_total_limit=2,
    )
    
    # Huấn luyện
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
    )
    
    trainer.train()
    
    # Lưu mô hình
    os.makedirs("models/fine_tuned_gpt2", exist_ok=True)
    model.save_pretrained("./models/fine_tuned_gpt2")
    tokenizer.save_pretrained("./models/fine_tuned_gpt2")
    
    print("Đã huấn luyện và lưu mô hình thành công!")

if __name__ == "__main__":
    train_model()