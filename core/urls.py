from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomePageView,name='home'),
    path('about_us/',views.AboutView,name='about'),
    path('services/',views.ServiceView,name='service')
]