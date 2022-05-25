from gc import get_objects

from buset.models import Posting
from django import template
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.generic import DetailView, ListView

from .forms import UserForm, PostForm
from .models import Posting
from django.db import connection

register = template.Library()

# Create your views here.
# class IndexView(generic.ListView):
#     # return HttpResponse("Index Landing Page.")
def MainView(request):
    context = {}
    context["posts"] = Posting.objects.all()
    return render(request,'buset/main.html',context)    
def PostView(request):
    # context_object_name = 'post'
    # queryset = Posting.objects.all()
    
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['post'] = Posting.objects.all()
    #     return context
    # post = get_object_or_404(Posting)
    form = PostForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        post = form.save()
        post.backend = 'django.contrib.auth.backends.ModelBackend'
        messages.success(request, "Berhasil!." )
        return redirect("post")
    return render(request=request,template_name='buset/post.html',context={'post_form':form})    
def register_proc(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, "Berhasil!." )
            return redirect("main")
        else:
            messages.error(request,"Ada error.")
        messages.error(request, "Registrasi gagal, ada yang salah nih!.")
    form = UserForm()
    return render (request=request, template_name="buset/register.html", context={"register_form":form})

def login_proc(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Selamat datang {username}.")
                return redirect("main")
            else:
                messages.error(request,"Kayaknya username atau password salah.")
        else:
            messages.error(request,"Kayaknya username atau password salah.")
    form = AuthenticationForm()
    return render(request=request, template_name="buset/login.html", context={"login_form":form})
def logout_proc(request):
    logout(request)
    messages.info(request, "Selamat tinggal!") 
    return redirect("main")

def CartView(request):
    # form = PostForm(request.POST)
    # if form.is_valid():
    #     post = form.save()
    #     post.backend = 'django.contrib.auth.backends.ModelBackend'
    #     messages.success(request, "Berhasil!." )
    #     return redirect("post")
    form = "s"
    return render(request=request,template_name='buset/cart.html',context={'post_form':form})  