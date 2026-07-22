from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'app1/home.html')

def index(request):
    return HttpResponse("<h1>Index Page</h1><p>This is the index page of app1.</p>")