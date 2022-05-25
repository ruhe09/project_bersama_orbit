from django.urls import path, include
from django.contrib import admin
from . import views
from django.conf import settings #add this
from django.conf.urls.static import static #add this
urlpatterns = [
    path('',views.MainView,name='main'),
    path('post/',views.PostView,name='post'),
    path('register',views.register_proc, name='register'),
    path('register/',views.register_proc, name='register'),
    path('login',views.login_proc, name='login'),
    path('logout',views.logout_proc, name='logout'),
    # path('profile',views.profile, name='profile'),
    path('accounts/', include('allauth.urls')),
    path('cart/', views.CartView, name='cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)