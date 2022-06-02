import io
from gc import get_objects
from buset.models import Posting
from django import template
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from PIL import Image as im
from .forms import Cv_Upload, PostForm, UserForm, ProfileForm
from .models import Cv_Model, Posting, Profile
import joblib
import pickle
import torch


register = template.Library()

class MainViewList(ListView):
    model = Posting
    template_name='buset/main.html'
class MainViewDetail(DetailView):
    model = Posting
    template_name='buset/detail.html'
    template_data={
        "profile":Profile.objects.all(),
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.all()
        return context
 

def PostView(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method =='POST':
        if form.is_valid():
            post = form.save(commit = False)
            post.user = request.user;
            post.save()
            post.backend = 'django.contrib.auth.backends.ModelBackend'
            form = PostForm()
            messages.success(request, "Berhasil!." )
            return redirect("post")
    return render(request,'buset/post.html',{'post_form':form})    

def register_proc(request):
    form = UserForm(request.POST)
    p_form = ProfileForm(request.POST)
    if request.method == "POST":
        form = UserForm(request.POST)
        p_form = ProfileForm(request.POST)
        if form.is_valid() and p_form.is_valid():
            user = form.save()
            p_form = p_form.save(commit=False)
            p_form.user = user
            p_form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, "Berhasil!" )
            return redirect("main")
        else:
            messages.error(request,"Ada error.")
        messages.error(request, "Registrasi gagal, ada yang salah nih!.")
    return render (request=request, template_name="buset/register.html", context={"register_form":form,"additional_form":p_form})

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

def FAQ(request):
    return render(request,'buset/faq.html')

def Cv_View(request):
    form = Cv_Upload(request.POST, request.FILES)
    if form.is_valid():
        img = request.FILES.get('image')
        img_instance = Cv_Model(
            image=img
        )
        img_instance.save()

        img_terbaru = Cv_Model.objects.filter().last()
        img_bytes = img_terbaru.image.read()
        img = im.open(io.BytesIO(img_bytes))


        path_hubconfig = "static/yolov5"
        path_weightfile = "static/best.pt" #hasil training
        model = torch.hub.load(path_hubconfig, 'custom',
                             path=path_weightfile, source='local')
        results = model(img, size=640)
        
        results.render()
        for img in results.imgs:
            img_base64 = im.fromarray(img)
            img_base64.save("media/yolo_out/gambar_predik.jpg", format="JPEG")

        hasil_predict_img = "/media/yolo_out/gambar_predik.jpg"

        form = Cv_Upload()
        context = {
            "layar": form,
            "predik": hasil_predict_img
        }
        return render(request, 'buset/layar.html', context)

    else:
        form = Cv_Upload()
    context = {
        "layar": form
    }
    return render(request, 'buset/layar.html', context)

