# chat/services.py

import requests
import urllib3

# SSL self-signed uyarılarını bastırmak için (gerektiğinde kaldırabilirsiniz):


class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api"

    def __init__(self, api_key):
        self.api_key = api_key

    def list_models(self):
        """
        OpenRouter’dan mevcut model listesini çeker.
        Dönen JSON’da önce 'data', sonra 'models' anahtarına bakar.
        """
        url = f"{self.BASE_URL}/v1/models"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        # verify=True bırakarak SSL sorununu da görebilirsiniz:
        resp = requests.get(url, headers=headers, timeout=15, verify=True)
        print("🛠 [list_models] status:", resp.status_code)
        print("🛠 [list_models] body  :", resp.text)
        resp.raise_for_status()

        data = resp.json()
        models = data.get("data") or data.get("models") or []
        print("🛠 [list_models] parsed models:", models)
        return [(m["id"], m.get("name", m["id"])) for m in models]

    def send_message(self, model_id, user_message, history=None):
        """
        Tek bir soru-cevap çalıştırır.
        history: [(role, content), ...] listesini OpenRouter formatına çevirir.
        """
        url = f"{self.BASE_URL}/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        messages = []

        if history:
            for role, content in history:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": user_message})

        payload = {"model": model_id, "messages": messages}
        resp = requests.post(url, json=payload, headers=headers, timeout=30, verify=True)
        print("🛠 [send_message] status:", resp.status_code)
        print("🛠 [send_message] body  :", resp.text)
        resp.raise_for_status()

        data = resp.json()
        return data["choices"][0]["message"]["content"]
