from django.urls import path

from . import views

app_name = 'vet'

urlpatterns = [
    path('', views.cita_list, name='cita_list'),
    path('nueva/', views.cita_crear, name='cita_crear'),
]
