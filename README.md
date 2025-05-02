# ChatForge

**ChatForge** is a Django-based desktop-style chat application that integrates with multiple AI backends (via OpenRouter). It features:

- 🎯 **Multiple AI models** (GPT-4.1 Mini, Claude 3.7, Qwen, Gemini, etc.)  
- 🔄 **Token-based pay-as-you-go billing**  
- 📂 **Persistent chat sessions** with rename & delete  
- 🔄 **Dynamic model list** with manual “Refresh models”  
- ⚙️ **User settings** (API key, default model)  
- 🖼️ **Copy-to-clipboard** on every message  
- 🎨 **Responsive, oval chat bubbles** & sidebar navigation  

---

## 🚀 Quick Start

### 1. Clone the repo  
```bash
git clone https://github.com/yonetici/chatforge-web.git
cd chatforge-web
```

### 2. Create & activate a Python virtual environment  
```bash
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies  
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Environment variables  
Create a `.env` in project root with:
```ini
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
OPENROUTER_API_KEY=your-openrouter-api-key
```

### 5. Apply migrations & create superuser  
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the development server  
```bash
python manage.py runserver
```

Browse to <http://127.0.0.1:8000/chat/> to start chatting!

---

## 🔧 Project Structure

```
chatforge-web/
├── accounts/              # User & settings app
│   ├── migrations/
│   ├── models.py          # AIModel, User (custom)
│   ├── views.py           # settings_view, refresh_models
│   └── templates/accounts/
│       └── settings.html
├── chat/                  # Chat app
│   ├── migrations/
│   ├── models.py          # ChatSession, Message
│   ├── services.py        # OpenRouterClient
│   ├── views.py           # session_list, session_detail, send, rename, delete
│   └── templates/chat/
│       ├── chat_base.html
│       └── session_detail.html
├── core/                  # Landing/home app (optional)
├── chatforge/             # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Features & Usage

### User Settings  
- **API key**: paste your OpenRouter key on **Settings** page  
- **Default model**: choose from the dropdown (dynamic or fallback list)  
- **Refresh models**: manually reload available models

### Chat Sessions  
- **New chat**: click **+ Yeni Sohbet** in sidebar  
- **Rename**: edit the title inline and ✓ to save  
- **Delete**: click 🗑 and confirm  
- **Sidebar**: shows all sessions with latest snippet & timestamp  

### In-Chat UI  
- **Oval chat bubbles** with pointer arrows  
- **Copy** any message via the 📋 icon  
- **Send** via button or Enter (Shift+Enter for newline)  
- **Auto-scroll** to latest message  

---

## 📦 Deployment

For production, consider:

1. Use **Gunicorn** + **Nginx** reverse proxy  
2. Set `DEBUG=False` and configure `ALLOWED_HOSTS`  
3. Securely store secrets (e.g. via environment variables)  
4. Serve static files with `collectstatic` & S3 or CDN  

Example Gunicorn command:
```bash
gunicorn chatforge.wsgi:application   --bind 0.0.0.0:8000   --workers 3
```

---

## 🤝 Contributing

1. Fork the repo  
2. Create a feature branch (`git checkout -b feature/YourFeature`)  
3. Commit your changes (`git commit -m "Add your feature"`)  
4. Push to your fork (`git push origin feature/YourFeature`)  
5. Open a Pull Request  

Please follow PEP 8 & Django best practices.

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
