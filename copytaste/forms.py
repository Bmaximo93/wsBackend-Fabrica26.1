from django import forms
from django.contrib.auth.models import User

class AddRecipeForm(forms.Form):
    youtube_url = forms.URLField(
        label='URL do Youtube',
        widget=forms.URLInput(attrs={'placeholder': 'https://www.youtube.com/watch?v=...'})
    )

