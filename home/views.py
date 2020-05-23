from django.shortcuts import render

def index(request):
    return render(request,'home.html')

def gendocs(request):
    return render(request,'gendocs.html')