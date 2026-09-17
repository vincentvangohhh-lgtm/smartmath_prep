import os
import httpx
from openai import OpenAI

class HermesService:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            # Lấy API key từ biến môi trường để bảo mật
            api_key = os.getenv("OPENROUTER_API_KEY")
            
            # Khởi tạo httpx.Client nhưng trust_env=False để ép không đọc bất kỳ proxy nào từ môi trường hệ thống
            transport = httpx.HTTPTransport(trust_env=False)
            custom_http_client = httpx.Client(transport=transport)
            
            cls._client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                http_client=custom_http_client
            )
        return cls._client

    @classmethod
    def ask_ai(cls, prompt: str, image_data: str = None) -> str:
        try:
            client = cls.get_client()
            
            messages_payload = [
                {"role": "system", "content": "Bạn là một trợ lý AI toán học thông minh cho dự án 12A3math. Luôn trả về công thức toán học chuẩn LaTeX."},
            ]
            
            if image_data:
                messages_payload.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_data}}
                    ]
                })
            else:
                messages_payload.append({
                    "role": "user",
                    "content": prompt
                })

            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=messages_payload,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            print("CHI TIẾT LỖI AI:", str(e))
            return f"Lỗi khi kết nối với AI: {str(e)}"