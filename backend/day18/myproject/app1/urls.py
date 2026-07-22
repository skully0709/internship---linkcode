from .views import *
from django.urls import path

urlpatterns = [
    path('home', home, name='home'),
    path('index/', index, name='index'),
    path("contact/", contact,name="contact"),
    path("about/", about,name="about")
]