import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserSettingsForm
from chat.services import OpenRouterClient
from .models import AIModel


FALLBACK_MODELS = [
    ('gpt-4.1-mini',   'GPT-4.1 Mini'),
    ('gpt-4o',         'GPT-4o'),
    ('claude-3.7',     'Claude 3.7 Sonnet'),
    ('gemini-2.5-pro', 'Gemini 2.5 Pro'),
]
@login_required
def settings_view(request):
    user = request.user

    db_list = list(AIModel.objects.values_list('model_id','name'))
    if db_list:
        choices = sorted(db_list, key=lambda x: x[1].lower())
    else:
        choices = FALLBACK_MODELS

    if request.method == 'POST' and 'save_settings' in request.POST:
        form = UserSettingsForm(request.POST, instance=user)
        form.fields['default_model'].choices = choices

        if form.is_valid():
            selected_id = form.cleaned_data['default_model']
            model_name = dict(choices).get(selected_id, selected_id)

            form.save()
            messages.success(
                request,
                f"Default model “{model_name}” has been saved."
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
        messages.error(request, "Please save your API key before proceeding.")
        return redirect('accounts:settings')

    try:
        client = OpenRouterClient(key)
        fetched = client.list_models()

        AIModel.objects.all().delete()
        for mid, name in fetched:
            AIModel.objects.create(model_id=mid, name=name)
        messages.success(request, f"{len(fetched)} new models available.")

    except requests.exceptions.SSLError as ssl_err:
        print("🛠 [refresh_models] SSL ERROR:", ssl_err)
        messages.error(
            request,
                "An error occurred during SSL certificate verification. "
                "Please check your network or SSL settings."
        )

    except requests.exceptions.RequestException as req_err:
        # Diğer HTTP/kütüphane hataları
        print("🛠 [refresh_models] REQUEST ERROR:", req_err)
        messages.error(
            request,
            f"A network error occurred while fetching the model list: {req_err}"
        )

    except Exception as e:
        # Beklenmedik genel hatalar
        print("🛠 [refresh_models] UNEXPECTED ERROR:", e)
        messages.error(
            request,
            f"Failed to update model list: {e}"
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
        messages.success(request, "Favorite models saved.")
        return redirect('accounts:favorites')

    return render(request, 'accounts/favorites.html', {
        'all_models':  all_models,
        'favorite_qs': favorite_qs,
    })