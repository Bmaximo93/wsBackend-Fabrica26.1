"""
URL configuration for copytaste_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from copytaste import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipes/', views.recipe_list_view, name='recipe_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recipes/add/', views.add_recipe_view, name='add_recipe'),
    path('recipes/<int:pk>/', views.recipe_detail_view, name='recipe_detail'),
    path('recipes/<int:pk>/delete/', views.delete_recipe_view, name='delete_recipe'),
    path('', views.recipe_list_view, name='recipe_list'),

]
