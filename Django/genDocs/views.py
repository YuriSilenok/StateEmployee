from django.http import HttpResponse

def index(request):
    return HttpResponse('Привет, привет !')

    
def test(request):
    return HttpResponse('Привет, тест!')