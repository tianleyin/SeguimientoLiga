from django.contrib import admin
from django.urls import path, include

from lliga import views
from .views import *

urlpatterns = [
    path('menu', views.menu, name="menu"),
    path('clasificacion/<int:lliga_id>',views.classificacio, name="classificacio"),
    path('crear_liga/', crear_liga, name='crear_liga'),
    path('crear_equipo/', crear_equipo, name='crear_equipo'),
    path('asignar_equipos_liga/', asignar_equipos_liga, name='asignar_equipos_liga'),
]

