from django.contrib import admin

from .models import Prestador


@admin.register(Prestador)
class PrestadorAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'rubro', 'tarifa', 'estado']
    list_filter = ['estado', 'rubro']
