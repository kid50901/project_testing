from django.urls import path
from . import views
 
urlpatterns = [
    path('callback', views.callback),
    path('pushbyurl', views.pushbyurl),
    #path('welcome', views.postfromhtml),
]