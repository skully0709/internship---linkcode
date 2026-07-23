from django.shortcuts import render

def home(request):
    return render(request, 'app1/home.html')

def gallery1(request):
    return render(request, 'app1/gallery1.html')

def gallery2(request):
    return render(request, 'app1/gallery2.html')

def gallery3(request):
    return render(request, 'app1/gallery3.html')