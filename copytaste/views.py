from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


# Create your views here.

def recipe_list_view(request):
    return render(request, 'recipe_list.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/') # TODO: criar /login/
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
