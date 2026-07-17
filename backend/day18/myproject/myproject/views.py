from django.http import HttpResponse
from django.shortcuts import render

def welcome(request):
    return HttpResponse("Welcome to my project!")

def bio(request):
    return HttpResponse("<h1>Bio Page</h1><p><strong>Name:</strong> Sarthak Patani</p><p><strong>Age:</strong> 18</p><p><strong>Intership:</strong> Linkcode Technologies</p>")

def index(request):
    return render(request, 'index.html')