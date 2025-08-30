import requests
import json

def api_call(url: str, prompt_text: str):
# принимает ссылку и текст, формирует параметры запроса и отправляет его
    # формируем параметры запроса, используя сообщение пользователя
    payload = {
        'model': 'gemma3:4b', # замените на свою модель
        "messages": [
            {
            "role": "user",
            "content": prompt_text,
            #"role": "system",
            #"content": "Ты полезный чат-бот по имени Gemma 3. Ты должен помогать пользователю."
            # content замените на свой системный промпт
            }
        ],
        'stream': False # запрещает модели давать ответ частями
    }

    # отправка запроса
    try:
        print(f"отправляю на {url} промпт: '{prompt_text}'")
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        
        data = response.json()
        # возращаем только ответ модели, без лишнего вывода
        return data.get('message', {}).get('content', 'не получилось извлечь ответ')

    except requests.RequestException as e:
        print(f"ошибка при запросе к апи: {e}")
        return "случилась ошибка при запросе к ИИ"