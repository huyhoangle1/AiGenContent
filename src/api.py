from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from generate_content import ContentGenerator
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class ContentRequest(BaseModel):
    topic: str
    tone: str = "thân thiện"
    length: int = 500
    keywords: list = []

@app.on_event("startup")
def startup_event():
    global generator
    model_path = os.getenv("MODEL_PATH", "./models/fine_tuned_gpt2")
    generator = ContentGenerator(model_path)

@app.post("/generate-content")
def generate_content_api(request: ContentRequest):
    try:
        content = generator.generate_and_optimize(
            topic=request.topic,
            tone=request.tone,
            keywords=request.keywords
        )
        
        if not content:
            raise HTTPException(status_code=500, detail="Failed to generate content")
        
        return {
            "status": "success",
            "content": content,
            "length": len(content.split()),
            "grammar_errors": generator.check_grammar(content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simple HTML form UI
@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!doctype html>
    <html lang=\"vi\">
    <head>
      <meta charset=\"utf-8\" />
      <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
      <title>AI Content Generator</title>
      <style>
        body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 2rem; }
        .container { max-width: 800px; margin: 0 auto; }
        label { display: block; margin: 0.5rem 0 0.25rem; font-weight: 600; }
        input, textarea, select { width: 100%; padding: 0.6rem; border: 1px solid #ccc; border-radius: 6px; }
        button { margin-top: 1rem; padding: 0.7rem 1rem; background: #2563eb; color: #fff; border: none; border-radius: 6px; cursor: pointer; }
        button:hover { background: #1d4ed8; }
        .card { padding: 1rem; border: 1px solid #e5e7eb; border-radius: 8px; background: #fafafa; }
      </style>
    </head>
    <body>
      <div class=\"container\">
        <h1>AI Content Generator</h1>
        <p>Nhập chủ đề và tuỳ chọn để tạo nội dung.</p>
        <form method=\"post\" action=\"/generate-form\" class=\"card\">
          <label for=\"topic\">Chủ đề</label>
          <input id=\"topic\" name=\"topic\" type=\"text\" placeholder=\"Ví dụ: công nghệ blockchain\" required />

          <label for=\"tone\">Giọng văn</label>
          <select id=\"tone\" name=\"tone\">
            <option value=\"thân thiện\">Thân thiện</option>
            <option value=\"trang trọng\">Trang trọng</option>
            <option value=\"thuyết phục\">Thuyết phục</option>
          </select>

          <label for=\"keywords\">Từ khoá (phân tách bằng dấu phẩy)</label>
          <input id=\"keywords\" name=\"keywords\" type=\"text\" placeholder=\"blockchain, an ninh mạng\" />

          <button type=\"submit\">Tạo nội dung</button>
        </form>
      </div>
    </body>
    </html>
    """

@app.post("/generate-form", response_class=HTMLResponse)
def generate_from_form(
    topic: str = Form(...),
    tone: str = Form("thân thiện"),
    keywords: str = Form("")
):
    try:
        keyword_list = [k.strip() for k in keywords.split(',') if k.strip()] if keywords else []
        content = generator.generate_and_optimize(
            topic=topic,
            tone=tone,
            keywords=keyword_list
        )
        if not content:
            raise HTTPException(status_code=500, detail="Failed to generate content")
        word_count = len(content.split())
        errors = generator.check_grammar(content)
        return f"""
        <!doctype html>
        <html lang=\"vi\">
        <head>
          <meta charset=\"utf-8\" />
          <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
          <title>Kết quả - AI Content Generator</title>
          <style>
            body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 2rem; }}
            .container {{ max-width: 900px; margin: 0 auto; }}
            .meta {{ color: #374151; margin-bottom: 1rem; }}
            .content {{ white-space: pre-wrap; padding: 1rem; border: 1px solid #e5e7eb; border-radius: 8px; background: #fff; }}
            a.button {{ display: inline-block; margin-top: 1rem; padding: 0.6rem 1rem; background: #2563eb; color: #fff; text-decoration: none; border-radius: 6px; }}
            a.button:hover {{ background: #1d4ed8; }}
          </style>
        </head>
        <body>
          <div class=\"container\">
            <h1>Kết quả</h1>
            <div class=\"meta\">Chủ đề: <strong>{topic}</strong> • Giọng văn: <strong>{tone}</strong> • Số từ: <strong>{word_count}</strong> • Lỗi ngữ pháp ước lượng: <strong>{errors}</strong></div>
            <div class=\"content\">{content}</div>
            <a class=\"button\" href=\"/\">← Tạo mới</a>
          </div>
        </body>
        </html>
        """
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host=host, port=port)