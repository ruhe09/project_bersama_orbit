from gc import get_objects
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.contrib.humanize.templatetags.humanize import intcomma
from django import template
from django.urls import reverse
from django.views import generic
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this

from buset.models import Posting
from .models import Posting

register = template.Library()

# Create your views here.
# class IndexView(generic.ListView):
#     # return HttpResponse("Index Landing Page.")
def MainView(request):
    return render(request,'buset/main.html')    
class PostView(DetailView):
    template_name = 'buset/pack/index.html'
    model = Posting
    # context_object_name = 'post'
    # queryset = Posting.objects.all()
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['post'] = Posting.objects.all()
        return context
    # post = get_object_or_404(Posting)
    # return render(request,'buset/pack/index.html',{'post':post})    

def register_proc(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("main")
        messages.error(request, "Unsuccessful registration. Invalid information.")
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
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="buset/login.html", context={"login_form":form})