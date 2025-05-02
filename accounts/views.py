from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserSettingsForm
from chat.services import OpenRouterClient

@login_required
def settings_view(request):
    user = request.user

    # POST: sadece form.save() ile hem api_key hem default_model kaydedeceğiz
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user)

        # POST’ta kesin choices ata ve enable et
        model_choices = []
        if request.user.openrouter_api_key or request.POST.get('openrouter_api_key'):
            # Örneğin yeni key POST içinde varsa, hem key hem seçim gönderilebilir
            api_key = request.POST.get('openrouter_api_key') or request.user.openrouter_api_key
            try:
                client = OpenRouterClient(api_key)
                model_choices = client.list_models()
                model_choices = sorted(model_choices, key=lambda x: x[1].lower())
            except:
                pass

        # POST’ta widget’ı enable et ki value gönderilsin
        form.fields['default_model'].choices = model_choices
        form.fields['default_model'].widget.attrs.pop('disabled', None)

        if form.is_valid():
            form.save()
            messages.success(request, "Ayarlar kaydedildi.")
            return redirect('accounts:settings')
    else:
        form = UserSettingsForm(instance=user)

    # GET: kayıtlı API key’e göre tekrar listeleyip disable/help-text uygula
    model_choices = []
    fetch_error = False
    if user.openrouter_api_key:
        try:
            client = OpenRouterClient(user.openrouter_api_key)
            model_choices = client.list_models()
        except:
            fetch_error = True

    field = form.fields['default_model']
    field.choices = model_choices
    if not user.openrouter_api_key:
        field.widget.attrs['disabled'] = True
        field.help_text = "Önce API anahtarını girip kaydetmelisiniz."
    elif fetch_error:
        field.widget.attrs['disabled'] = True
        field.help_text = "Modeller yüklenemedi. API anahtarınızı kontrol edin."
    elif not model_choices:
        field.widget.attrs['disabled'] = True
        field.help_text = "Henüz kullanılabilir model bulunamadı."
    else:
        field.widget.attrs.pop('disabled', None)
        field.help_text = ""

    return render(request, 'accounts/settings.html', {'form': form})
