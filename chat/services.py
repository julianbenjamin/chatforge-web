# chat/services.py
import requests

class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api"

    def __init__(self, api_key):
        self.api_key = api_key

    def send_message(self, model_id, user_message, history=None):
        url = f"{self.BASE_URL}/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        messages = []
        if history:
            for role, content in history:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": user_message})
        payload = {"model": model_id, "messages": messages}

        #resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp = requests.post(url, json=payload, headers=headers, timeout=30, verify=False)

        # **Debug:**
        print("🛠 [send_message] status:", resp.status_code)
        print("🛠 [send_message] response:", resp.text)

        try:
            resp.raise_for_status()
        except requests.HTTPError:
            # 4xx veya 5xx geldiğinde JSON içinde hata detayları olabilir
            raise

        data = resp.json()

        if "choices" not in data:
            # API bize hata döndüyse, ya da format değiştiyse
            err = data.get("error", data)
            raise ValueError(f"OpenRouter response has no choices: {err!r}")

        return data["choices"][0]["message"]["content"]
