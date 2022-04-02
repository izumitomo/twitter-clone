from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('mypage/', views.mypage, name='mypage'),
]
