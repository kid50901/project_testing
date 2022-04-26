"""Financial_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path
from myapp import views 
urlpatterns = [
    #url（r'^'，include（'django.contrib.auth.urls'）），
    path('admin/', admin.site.urls),
    path('initAssetsByURL', views.initAssetsByURL),
    path('initIcomeByURL', views.initIncomeByURL),
    path('updateEndMeetsByURL', views.updateEndMeetsByURL),
    path('base', views.base),
    path('test', views.test),
    path('querytable_assets', views.querytable_assets),
    path('querytable_income', views.querytable_income),
    path('querytable_endMeets', views.querytable_endMeets),
    path('lazyupdate_assets', views.lazyupdate_assets),
    path('lazyupdate_income', views.lazyupdate_income),
    path('lazydelete_income', views.lazydelete_income),
    path('lazydelete_assets', views.lazydelete_assets),
    path('lazy_borad_data', views.lazy_borad_data),
    path('lazy_board', views.lazy_board),
    path('lazyupdate_debt', views.lazyupdate_debt),
    path('lazydelete_debt', views.lazydelete_debt),
    #path('index/',  views.index),
    path('accounts/login/', auth_views.LoginView.as_view()),
    path('accounts/logout/', auth_views.LogoutView.as_view()),
    path('accounts/profile/', views.index),
]
