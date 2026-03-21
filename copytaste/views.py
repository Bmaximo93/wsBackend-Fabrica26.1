from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import Http404
from django.shortcuts import render, redirect

from copytaste.forms import AddRecipeForm, EditRecipeForm
from copytaste.gemini import extract_recipe_from_video
from copytaste.models import Recipe


# Create your views here.

def recipe_list_view(request):
    return render(request, 'recipe_list.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/recipes/')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required
def recipe_list_view(request):
    recipes = Recipe.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'recipe_list.html', {'recipes': recipes})

@login_required
def add_recipe_view(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['youtube_url']
            try:
                recipe_data = extract_recipe_from_video(url)
                Recipe.objects.create(
                    user=request.user,
                    title=recipe_data.title,
                    description=recipe_data.description,
                    summary=recipe_data.summary,
                    ingredients=recipe_data.ingredients,
                    steps=recipe_data.steps,
                    duration_minutes=recipe_data.duration_minutes,
                    source_url=url,
                )
                return redirect('/recipes/')
            except Exception as e:
                error_msg = str(e)
                if 'Cannot fetch content' in error_msg:
                    error_msg = 'Não foi possivel acessar o vídeo. Verifique se a URL é válida.'
                form.add_error(None, error_msg)
    else:
        form = AddRecipeForm()

    return render(request, 'add_recipe.html', {'form': form})

@login_required
def recipe_detail_view(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk, user=request.user)
    except Recipe.DoesNotExist:
        raise Http404
    return render(request, 'recipe_detail.html', {'recipe': recipe})

@login_required
def delete_recipe_view(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk, user=request.user)
    except Recipe.DoesNotExist:
        return redirect('/recipes/')

    recipe.delete()
    return redirect('/recipes/')

@login_required
def edit_recipe_view(request, pk):
    recipe = Recipe.objects.get(pk=pk, user=request.user)

    if request.method == 'POST':
        form = EditRecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = EditRecipeForm(instance=recipe)

    return render(request, 'edit_recipe.html', {'form': form, 'recipe': recipe})


