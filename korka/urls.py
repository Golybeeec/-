from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('applications/', views.applications_list, name='applications_list'),
    path('applications/create/', views.application_create, name='application_create'),
    
]