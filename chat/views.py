# chat/views.py
import json
import requests 
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import ChatSession, Message
from chat.services import OpenRouterClient
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def rename_session(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    new_title = request.POST.get("title", "").strip()
    if new_title:
        session.title = new_title
        session.save()
        messages.success(request, f"Sohbet başlığı “{new_title}” olarak güncellendi.")
    else:
        messages.error(request, "Geçersiz başlık.")
    return redirect("chat:session_detail", pk=pk)

@login_required
@require_POST
def delete_session(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    session.delete()
    messages.success(request, "Sohbet silindi.")
    return redirect("chat:session_list")
@login_required
def session_list(request):
    # boş bir “session” tanımlayıp direkt yeni oturum oluşturma linki gösterebilir
    return render(request, 'chat/chat_base.html', {
        'session': None,  # sidebar için
    })
@login_required
def session_detail(request, pk):
    session   = get_object_or_404(ChatSession, pk=pk, user=request.user)
    favorites = request.user.favorite_models.all()
    return render(request, 'chat/session_detail.html', {
        'session':        session,
        'favorite_models': favorites,
    })
@login_required
def new_session(request):
    # Yeni bir oturum oluştur, başlık olarak tarih/kullanıcı seçebilirsin
    session = ChatSession.objects.create(
        user=request.user,
        title="Yeni Sohbet"
    )
    return redirect('chat:session_detail', pk=session.pk)
@login_required
@require_POST
def send_message(request, session_id):
    session = get_object_or_404(ChatSession, pk=session_id, user=request.user)
    try:
        payload = json.loads(request.body)
        user_text = payload.get("message","").strip()
        if not user_text:
            return JsonResponse({"error":"Mesaj boş olamaz"}, status=400)

        # Kullanıcı mesajı
        user_msg = Message.objects.create(session=session, is_user=True, content=user_text)

        # AI cevabı
        client = OpenRouterClient(request.user.openrouter_api_key)
        ai_text = client.send_message(request.user.default_model, user_text)

        ai_msg = Message.objects.create(session=session, is_user=False, content=ai_text)

        return JsonResponse({
            "user": {"id": user_msg.id, "content": user_msg.content, "timestamp": user_msg.timestamp},
            "ai":   {"id": ai_msg.id,   "content": ai_msg.content,   "timestamp": ai_msg.timestamp},
        })

    except ValueError as ve:
        # choices eksik vs. kontrollü hata
        return JsonResponse({"error": str(ve)}, status=502)

    except requests.HTTPError as he:
        # HTTP 4xx/5xx hataları
        return JsonResponse({"error": f"API error: {he}"}, status= he.response.status_code)

    except Exception as e:
        # Diğer beklenmedik hatalar
        return JsonResponse({"error": f"Sunucu hatası: {e}"}, status=500)
    
@login_required
def session_list(request):
    sessions = ChatSession.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "chat/session_list.html", {"sessions": sessions})

@login_required
def session_detail(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    return render(request, "chat/session_detail.html", {"session": session})
