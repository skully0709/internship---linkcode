from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('gallery1/', views.gallery1, name='gallery1'),
    path('gallery2/', views.gallery2, name='gallery2'),
    path('gallery3/', views.gallery3, name='gallery3'),
]