from django import forms
from django.contrib.auth.forms import UserCreationForm

from copytaste.models import Recipe

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None

class AddRecipeForm(forms.Form):
    youtube_url = forms.URLField(
        label='URL do Youtube',
        widget=forms.URLInput(attrs={'placeholder': 'https://www.youtube.com/watch?v=...'})
    )

class EditRecipeForm(forms.ModelForm):
    ingredients = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6}),
        label='Ingredients (um por linha)',
    )
    steps = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 8}),
        label='Passos (um por linha)',
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'summary', 'duration_minutes', 'ingredients', 'steps']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if isinstance(self.instance.ingredients, list):
                self.initial['ingredients'] = '\n'.join(self.instance.ingredients)
            if isinstance(self.instance.steps, list):
                self.initial['steps'] = '\n'.join(self.instance.steps)

    def clean_ingredients(self):
        text = self.cleaned_data['ingredients']
        return [line.strip() for line in text.splitlines() if line.strip()]

    def clean_steps(self):
        text = self.cleaned_data['steps']
        return [line.strip() for line in text.splitlines() if line.strip()]
