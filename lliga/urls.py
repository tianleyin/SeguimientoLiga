from django.contrib import admin
from django.urls import path, include

from lliga import views

urlpatterns = [
    path('menu', views.menu, name="menu"),
    path('clasificacion/<int:lliga_id>',views.classificacio, name="classificacio")
]

