"""djangoforum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.urls import re_path
from boards import views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.home, name='home'),
    re_path('signup/$', accounts_views.signup, name='signup'),
    #LoginView直接查找template_name为login.html的页面
    re_path('login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path('logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path('boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    re_path(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    path('admin/', admin.site.urls),

]
