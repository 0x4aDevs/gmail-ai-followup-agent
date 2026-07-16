import os

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - dependency is optional until installed
    genai = None


SAMPLE_EMAIL_TEXT = """
Subject: Запрос по договору

Здравствуйте,

Нужна помощь с актуальным статусом по договору №12345.
Мы уже обсуждали сроки и хотели бы понять, когда можно ожидать финальный ответ.
"""


def send_email_to_gemini(email_text: str = SAMPLE_EMAIL_TEXT) -> str:
    """
    Отправляет текст письма в Gemini.

    Параметры:
        email_text: текст письма. По умолчанию используется заглушка в коде.

    Возвращает:
        строковый ответ модели Gemini.
    """
    if genai is None:
        raise ImportError("Установите зависимость `google-generativeai`.")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Переменная окружения GEMINI_API_KEY не задана.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = (
        "Ты — помощник, который анализирует электронные письма. "
        "Сделай краткое резюме письма и выдели ключевой запрос клиента.\n\n"
        f"Текст письма:\n{email_text}"
    )

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    print(send_email_to_gemini())