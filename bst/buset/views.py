from gc import get_objects
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from buset.models import Posting
from django.template import loader
from .models import Posting
from django.contrib.humanize.templatetags.humanize import intcomma
from django import template

register = template.Library()

# Create your views here.
def index(request):
    return HttpResponse("Index Landing Page.")
def post(request):
    post = get_object_or_404(Posting)
    return render(request,'buset/pack/index.html',{'post':post})    
def currency(IDR):
    idr = round(float(IDR), 2)
    return "Rp. %s%s" % (intcomma(int(IDR)), ("%0.2f" % IDR)[-3:])
register.filter('currency', currency)    
    