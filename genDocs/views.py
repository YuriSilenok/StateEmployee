from django.shortcuts import render

import os

app_name = 'gendocs'
def index(request):
    templates = os.path.join(app_name,'index.html')
    print(templates)
    return render(request,templates)