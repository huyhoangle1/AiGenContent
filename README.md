# AI Content Generator

Hệ thống AI tự động tạo nội dung sử dụng mô hình GPT-2

## Cài đặt
1. Tạo môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt

# Xử lý dữ liệu
python src/data_processing.py

# Huấn luyện mô hình
python src/train_model.py

# Chạy API
python src/api.py

{
  "topic": "công nghệ blockchain",
  "tone": "trang trọng",
  "keywords": ["blockchain", "an ninh mạng"]
}


python -m pytest tests/"# AiGenContent" 
