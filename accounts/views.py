import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserSettingsForm
from chat.services import OpenRouterClient
from .models import AIModel

# --- Statik yedek model listesi ---
FALLBACK_MODELS = [
    ('gpt-4.1-mini',   'GPT-4.1 Mini'),
    ('gpt-4o',         'GPT-4o'),
    ('claude-3.7',     'Claude 3.7 Sonnet'),
    ('gemini-2.5-pro', 'Gemini 2.5 Pro'),
    # ihtiyaç oldukça ekleyebilirsin
]
@login_required
def settings_view(request):
    user = request.user

    # 1) Mevcut DB listesini veya fallback’i al
    db_list = list(AIModel.objects.values_list('model_id','name'))
    if db_list:
        choices = sorted(db_list, key=lambda x: x[1].lower())
    else:
        choices = FALLBACK_MODELS

    # 2) POST ise formu başlat ve mutlaka choices ata
    if request.method == 'POST' and 'save_settings' in request.POST:
        form = UserSettingsForm(request.POST, instance=user)
        form.fields['default_model'].choices = choices

        if form.is_valid():
            # Seçilen modelin id’si
            selected_id = form.cleaned_data['default_model']
            # choices’dan label’ını bul
            model_name = dict(choices).get(selected_id, selected_id)

            form.save()
            messages.success(
                request,
                f"Varsayılan model “{model_name}” olarak kaydedildi."
            )
            return redirect('accounts:settings')
    else:
        form = UserSettingsForm(instance=user)
        form.fields['default_model'].choices = choices

    return render(request, 'accounts/settings.html', {'form': form})

@login_required
def refresh_models(request):
    key = request.user.openrouter_api_key
    if not key:
        messages.error(request, "Önce API anahtarınızı kaydetmelisiniz.")
        return redirect('accounts:settings')

    try:
        client = OpenRouterClient(key)
        # Burada verify=True olduğu için SSL hatası fırlarsa SSLError yakalanacak
        fetched = client.list_models()

        # Başarılı ise DB’yi güncelle
        AIModel.objects.all().delete()
        for mid, name in fetched:
            AIModel.objects.create(model_id=mid, name=name)
        messages.success(request, f"{len(fetched)} model yüklendi.")

    except requests.exceptions.SSLError as ssl_err:
        # SSL’e özel hata bloğu
        print("🛠 [refresh_models] SSL ERROR:", ssl_err)
        messages.error(
            request,
            "SSL sertifika doğrulaması sırasında bir hata oluştu. "
            "Lütfen ağ veya SSL ayarlarınızı kontrol edin."
        )

    except requests.exceptions.RequestException as req_err:
        # Diğer HTTP/kütüphane hataları
        print("🛠 [refresh_models] REQUEST ERROR:", req_err)
        messages.error(
            request,
            f"Model listesi alınırken bir ağ hatası oluştu: {req_err}"
        )

    except Exception as e:
        # Beklenmedik genel hatalar
        print("🛠 [refresh_models] UNEXPECTED ERROR:", e)
        messages.error(
            request,
            f"Model listesi güncellenemedi: {e}"
        )

    return redirect('accounts:settings')

@login_required
def favorites_view(request):
    user       = request.user
    all_models = AIModel.objects.order_by('name')
    favorite_qs = user.favorite_models.values_list('model_id', flat=True)

    if request.method == 'POST':
        selected = request.POST.getlist('favorites')
        qs = AIModel.objects.filter(model_id__in=selected)
        user.favorite_models.set(qs)
        messages.success(request, "Favori modelleriniz güncellendi.")
        return redirect('accounts:favorites')

    return render(request, 'accounts/favorites.html', {
        'all_models':  all_models,
        'favorite_qs': favorite_qs,
    })