from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.MainView,name='main'),
    path('post/',views.PostView.as_view(),name='post'),
    path('register',views.register_proc, name='register'),
    path('register/',views.register_proc, name='register'),
    path('login',views.login_proc, name='login'),
    path('accounts/', include('allauth.urls')),
]