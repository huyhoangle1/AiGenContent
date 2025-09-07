from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import language_tool_python
import logging
from datetime import datetime
import os

# Tải tài nguyên NLTK
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Thiết lập logging
logging.basicConfig(
    filename='logs/ai_content_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ContentGenerator:
    def __init__(self, model_path="./models/fine_tuned_gpt2"):
        self.generator = pipeline('text-generation', model=model_path)
        self.grammar_tool = language_tool_python.LanguageTool('vi')
        self.stop_words = set(stopwords.words('vietnamese'))
    
    def create_prompt(self, topic, tone="thân thiện", length=500):
        return f"Hãy viết một bài {length} từ về {topic} với giọng văn {tone}: "
    
    def generate_content(self, topic, tone="thân thiện", max_length=600):
        try:
            prompt = self.create_prompt(topic, tone)
            result = self.generator(
                prompt,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                top_k=50,
                top_p=0.95
            )
            content = result[0]['generated_text'].replace(prompt, "")
            
            # Ghi log thành công
            logging.info(f"Generated content for topic: {topic}")
            return content
        except Exception as e:
            logging.error(f"Error generating content: {str(e)}")
            return None
    
    def optimize_seo(self, text, keywords):
        # Thêm từ khóa vào đầu/cuối đoạn
        if keywords:
            text = f"{keywords[0]}. {text} {keywords[-1]}"
        
        # Xóa stopwords (tùy chọn)
        words = word_tokenize(text)
        filtered_text = ' '.join([w for w in words if not w in self.stop_words])
        
        return filtered_text
    
    def check_grammar(self, text):
        matches = self.grammar_tool.check(text)
        return len(matches)
    
    def generate_and_optimize(self, topic, tone="thân thiện", keywords=None):
        content = self.generate_content(topic, tone)
        if content and keywords:
            content = self.optimize_seo(content, keywords)
        return content

if __name__ == "__main__":
    generator = ContentGenerator()
    content = generator.generate_and_optimize(
        topic="lợi ích của năng lượng mặt trời",
        keywords=["năng lượng sạch", "bảo vệ môi trường"]
    )
    print(content)