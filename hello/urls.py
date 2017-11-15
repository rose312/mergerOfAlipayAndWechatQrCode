# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pay/', views.pay, name='pay'),
]
