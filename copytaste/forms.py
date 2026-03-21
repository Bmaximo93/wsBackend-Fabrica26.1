from django import forms

from copytaste.models import Recipe


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

    def clean_ingredients(self):
        text = self.cleaned_data['ingredients']
        return [line.strip() for line in text.splitlines() if line.strip()]

    def clean_steps(self):
        text = self.cleaned_data['steps']
        return [line.strip() for line in text.splitlines() if line.strip()]
