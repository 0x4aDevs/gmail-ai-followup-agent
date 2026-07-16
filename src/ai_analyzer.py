# Copyright (C) 2026 0x4aDevs
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os 
from pydantic import BaseModel, Field

try:
    import google.generativeai as genai
    import google.generativeai.types as genai_types
except ImportError:
    genai = None
    genai_types = None

SAMPLE_EMAIL_TEXT = """
Subject: Запрос по договору

Здравствуйте,

Нужна помощь с актуальным статусом договора. Пожалуйста, предоставьте информацию о текущем состоянии и сроках выполнения.
"""

# Что мы собственно хотим получить от аишника в этом случае он пишет НАМ что было в письме и какие рекомендуемые действия...
class EmailAnalysis(BaseModel):
    summary: str = Field(..., description="Краткое содержание письма")
    key_requests: list[str] = Field(..., description="Основные запросы или вопросы, содержащиеся в письме")
    needs_follow_up: bool = Field(..., description="Нужно ли отправлять follow-up письмо")
    follow_up_suggestions: list[str] = Field(..., description="Предложения по follow-up письму, если нужно")
    rank: int = Field(..., description="Рейтинг письма по важности (1-10)")

def analyze_email_structured(email_text: str = SAMPLE_EMAIL_TEXT) -> EmailAnalysis:
    if genai is None:
        raise ImportError("google.generativeai module is not installed. Please install it to use this function.")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.") 

    genai.configure(api_key=api_key)

    # Используем ИИшник который нам доступен, в данном случае Геминий ( я надеюсь не ошибся с названием модели...)
    model = genai.GenerativeModel("gemini-3.1")

    prompt = ( 
        "Ты помощник который анализирует электронные письма."
        "Твоя задача - прочитать письмо и предоставить структурированный анализ в формате JSON, который соответствует следующей схеме:\n"
        f"Текст письма: \n{email_text}\n\n"
        "Заполни структуру следующими данными:\n"
        "{\n"
        "  'summary': 'Краткое содержание',\n"
        "  'key_requests': ['Основные запросы или вопросы, содержащиеся в письме'],\n"
        "  'needs_follow_up': true/false,\n"
        "  'follow_up_suggestions': ['Предложения по follow-up письму, если нужно'],\n"
        "  'rank': 1-10\n"
        "}"
    )

    response = model.generate_content(
        prompt,
        generation_config=genai_types.GenerationConfig(
            response_mime_type="application/json",
            response_schema=EmailAnalysis,
        ),
    )
    return response.text

if __name__ == "__main__":
    json_result = analyze_email_structured()
    print(json_result)