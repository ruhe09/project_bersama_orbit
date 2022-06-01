from django.urls import path, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import MainViewList, MainViewDetail
urlpatterns = [
    path('',MainViewList.as_view(),name='main'),
    path('post/<slug:slug>',MainViewDetail.as_view(),name='article_detail'),
    path('post/',views.PostView,name='post'),
    path('register',views.register_proc, name='register'),
    path('register/',views.register_proc, name='register'),
    path('login',views.login_proc, name='login'),
    path('login/',views.login_proc, name='login'),
    path('logout',views.logout_proc, name='logout'),
    # path('profile',views.profile, name='profile'),
    path('accounts/', include('allauth.urls')),
    path('cart/', views.CartView, name='cart'),
    path('layar/', views.Cv_View, name='layar'),
    path('faq/', views.FAQ, name='faq'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)