from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'dogpark/index.html', context=context_dict)

def user_login():
    pass

def user_logout():
    pass

def register(request):
    return render(request, 'dogpark/register.html', context={})

def dashboard():
    pass
