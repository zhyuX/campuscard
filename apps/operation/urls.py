"""campuscard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
# from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
import xadmin

from operation.views import borrowingView,consumpView,entrance_guardView, IndexView


urlpatterns = [
    #path('admin/', xadmin.site.urls),
    path('borrowing/', borrowingView.as_view(), name='borrowing'),
    path('consump/', consumpView.as_view(), name='consump'),
    path('entrance_guard/', entrance_guardView.as_view(), name='entrance_guard'),
    path('index/', IndexView.as_view(), name='index')

]
