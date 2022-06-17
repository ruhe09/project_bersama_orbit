import io
import json
import pickle
import random
from gc import get_objects
from urllib import request
import cv2
import imutils
import joblib
import nltk
import numpy as np
import requests
import torch
from buset.models import Posting
from django import template
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import connection
from django.http import (HttpRequest, HttpResponse, HttpResponseServerError,
                         StreamingHttpResponse, JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
from PIL import Image as im

from .forms import (Bunga_Upload, Cv_Upload, PostForm, ProfileForm,
                    ProfileImgUpdtForm, ProfileUpdtForm, UserForm,
                    UserUpdtForm)
from .models import Bunga_Model, Cv_Model, Posting, Profile
from django.http import QueryDict
lemmatizer = WordNetLemmatizer()
register = template.Library()

def cari(request):
        if request.method =="GET" or "POST":
            # urlip = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyB3Wnrze0nVSxFKyVDIUKgp_6k2DrKyf4Q"
            # responseip = requests.request("POST",urlip)
            # querloc = responseip.json()
            # lat=querloc['results']['geometry']['location']
            # lang=querloc['location']['lang']
            form = request.GET["textcari"]
            API_KEY = "AIzaSyB3Wnrze0nVSxFKyVDIUKgp_6k2DrKyf4Q"
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={form}&type=service&key={API_KEY}"
            response = requests.request("GET",url)
            quer = response.json()
            context=quer['results']

            urly = f"https://www.googleapis.com/youtube/v3/search?q={form}&key={API_KEY}"
            responsey = requests.request("GET",urly)
            query = responsey.json()
            contexty=query['items']

            # urlph = f"https://maps.googleapis.com/maps/api/place/details/json?placeid={jalan}&key=AIzaSyB3Wnrze0nVSxFKyVDIUKgp_6k2DrKyf4Q"
            # responseph = requests.request("GET",urlph)
            # querph = responseph.json()
            # contextph=querph['results']
            # ph=querph['results']['international_phone_number']
        return render(request,'buset/cari.html',
                      {
                          'quer':quer,
                          'context':context,
                          'cari':url,
                          'range':range(20),
                          'youtube':contexty,
                          'form':form,
                          
                          }
                      )  

class MainViewList(ListView):
    model = Posting
    template_name='buset/main.html'

    def get_context_data(self,**kwargs):
        API_KEY = "AIzaSyB3Wnrze0nVSxFKyVDIUKgp_6k2DrKyf4Q"
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJ66K-CDjmaC4R_o1bWc2jHL8&key={API_KEY}"
        response = requests.request("GET",url)
        quer = response.json()
        context = super(MainViewList,self).get_context_data(**kwargs)
        context['context']= quer['result']
        return context
class MainViewDetail(DetailView):
    model = Posting
    template_name='buset/detail.html'
    template_data={
        "profile":Profile.objects.filter(),
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter()
        return context
 
@login_required
def PostView(request):
    
    
    if request.method =='POST':
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.save(commit = False)
            post.user = request.user;
            post.save()
            post.backend = 'django.contrib.auth.backends.ModelBackend'
            form = PostForm()
            messages.success(request, "Berhasil!" )
            return redirect("post")
        
    form = PostForm()
    return render(request,'buset/post.html',{'post_form':form})    

def register_proc(request):
   
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
    form = UserForm(request.POST)
    p_form = ProfileForm(request.POST)
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


@login_required
def profile_page(request):
    context = {
        "posting":Posting.objects.all(),
    }
    return render (request=request, template_name="buset/profile.html", context=context)
    
    
@login_required
def profile_update_proc(request):
    if request.method == "POST":
        form = UserUpdtForm(request.POST,instance = request.user)
        p_form = ProfileUpdtForm(request.POST, request.FILES, instance = request.user.profile)
        if form.is_valid() and p_form.is_valid():
            u_form = form.save(commit=False)
            u_form.user = request.user
            u_form.save()
            u_form.backend = 'django.contrib.auth.backends.ModelBackend'
            a_form = p_form.save(commit=False)
            a_form.user = request.user
            a_form.save()
            messages.success(request, 'Akun diperbarui!')
            return redirect('profile')
        else:
            messages.error(request,"gagal")

    form = UserUpdtForm(instance = request.user)
    p_form = ProfileUpdtForm(instance = request.user.profile)
    context = {
        'update_form': form,
        'additional_form':p_form,
    }
    return render(request, 'buset/profile_update.html', context)

@login_required
def profile_img_update_proc(request):
    if request.method =='POST':
        form = ProfileImgUpdtForm(request.POST or None, request.FILES or None,instance = request.user)
        if form.is_valid():
            post = form.save(commit = False)
            post.user = request.user.profile
            post.save()
            post.backend = 'django.contrib.auth.backends.ModelBackend'
            messages.success(request, "Berhasil!" )
            return redirect("profile_image")

    form = ProfileImgUpdtForm(instance = request.user)
    context = {
        'additional_form':form,
    }
    return render(request, 'buset/profile_update.html', context)

def logout_proc(request):
    logout(request)
    messages.info(request, "Selamat tinggal!") 
    return redirect("main")

@login_required
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
    form = Cv_Upload(request.POST or None, request.FILES)
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

def Bunga_View(request):
    form = Bunga_Upload(request.POST, request.FILES)
    if form.is_valid():
        img = request.FILES.get('image')
        img_instance = Bunga_Model(
            image=img
        )
        img_instance.save()

        img_terbaru = Bunga_Model.objects.filter().last()
        img_bytes = img_terbaru.image.read()
        img = im.open(io.BytesIO(img_bytes))


        path_hubconfig = "static/yolov5"
        path_weightfile = "static/bunga/best.pt" #hasil training
        model = torch.hub.load(path_hubconfig, 'custom',
                             path=path_weightfile, source='local')
        results = model(img, size=640)
        
        results.render()
        for img in results.imgs:
            img_base64 = im.fromarray(img)
            img_base64.save("media/yolo_out/gambar_predik.jpg", format="JPEG")

        hasil_predict_img = "/media/yolo_out/gambar_predik.jpg"

        form = Bunga_Upload()
        context = {
            "bunga": form,
            "predik": hasil_predict_img
        }
        return render(request, 'buset/bunga.html', context)

    else:
        form = Bunga_Upload()
    context = {
        "bunga": form
    }
    return render(request, 'buset/bunga.html', context)
def ChatView(request):
    userText = request.GET.get("msg",'')
    model = load_model('static/chatbot/chatbot_model.h5')
    intents = json.loads(open('static/chatbot/intents.json').read())
    words = pickle.load(open('static/chatbot/words.pkl','rb'))
    classes = pickle.load(open('static/chatbot/classes.pkl','rb'))


    def clean_up_sentence(sentence):
        # tokenize the pattern - split words into array
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word - create short form for word
        sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    def bow(sentence, words, show_details=True):
        # tokenize the pattern
        sentence_words = clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(words)  
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s: 
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print ("found in bag: %s" % w)
        return(np.array(bag))

    def predict_class(sentence, model):
        # filter out predictions below a threshold
        p = bow(sentence, words,show_details=False)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        return return_list

    def getResponse(ints, intents_json):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
        return result

    def chatbot_response(msg):
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
        return res

    context =   {
        'status': 1,
        'response': chatbot_response(userText),
    } 
    return JsonResponse(context)


camera = cv2.VideoCapture(0)  


def gen_frames_2():  
    while True:
        success, frame = camera.read() 
        if not success:
            break
        else:
            frame = imutils.resize(frame, width=128)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            path_hubconfig = "static/yolov5"
            path_weightfile = "static/bunga/best.pt"
            model = torch.hub.load(path_hubconfig, 'custom',
                                path=path_weightfile, source='local')
            results = model(gray, size=128)
            results.render()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result





def VideoView(request):
    return StreamingHttpResponse(gen_frames_2(),content_type="multipart/x-mixed-replace;boundary=frame")
