from django.shortcuts import render

# Create your views here.

def recipe_list_view(request):
    return render(request, 'recipe_list.html')
