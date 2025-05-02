from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSettingsForm(forms.ModelForm):
    default_model = forms.ChoiceField(label="Model", choices=[], required=False,
        widget=forms.Select(attrs={'class':'form-select'}))

    class Meta:
        model = User
        fields = ['openrouter_api_key', 'default_model']
        widgets = {
            'openrouter_api_key': forms.TextInput(attrs={'class':'form-control'}),
        }
