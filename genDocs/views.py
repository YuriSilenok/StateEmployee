from django.http import HttpResponse

def index(request):
    return HttpResponse('Привет, привет !')

    
def new(request):
    return HttpResponse('Привет, тест!')