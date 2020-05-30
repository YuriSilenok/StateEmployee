from django.shortcuts import render
import os

def index(request):    
    return render(request,os.path.join('home','index.html'))

def gendocs(request):
    return render(request,os.path.join('home','gendocs.html'))