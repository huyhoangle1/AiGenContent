
import pandas as pd
from sklearn.model_selection import train_test_split
import re
import os

def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = text.lower()
    return text

def process_data():
    # Tạo dữ liệu mẫu nếu chưa có
    if not os.path.exists("data/raw/content_data.csv"):
        sample_data = {
            "text": [
                "Năng lượng mặt trời là nguồn năng lượng sạch và bền vững",
                "Công nghệ AI đang thay đổi cách chúng ta làm việc",
                "Blockchain mang lại giải pháp bảo mật cao cho giao dịch"
            ],
            "category": ["công nghệ", "công nghệ", "công nghệ"],
            "tone": ["trang trọng", "thân thiện", "trang trọng"]
        }
        pd.DataFrame(sample_data).to_csv("data/raw/content_data.csv", index=False)
    
    # Đọc và xử lý dữ liệu
    data = pd.read_csv("data/raw/content_data.csv")
    data["clean_text"] = data["text"].apply(clean_text)
    
    # Tách train/test
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
    
    # Lưu dữ liệu đã xử lý
    os.makedirs("data/processed", exist_ok=True)
    train_data.to_csv("data/processed/train_data.csv", index=False)
    test_data.to_csv("data/processed/test_data.csv", index=False)
    
    print("Đã xử lý dữ liệu thành công!")

if __name__ == "__main__":
    process_data()