# ==================================================================
# GUIA: ARCHIVO  biblioteca/forms.py
# LAB     : 07 Parte 2 (biblioteca)
# EJERCICIO: formulario de la pantalla 'Registrar prestamo'
# QUE HACE : PrestarForm pide socio, libro y dias (1-60); lo procesa views.prestamo_registrar.
# ==================================================================
from django import forms

from .models import Libro, Socio


class PrestarForm(forms.Form):
    socio = forms.ModelChoiceField(queryset=Socio.objects.all(), label='Socio')
    libro = forms.ModelChoiceField(queryset=Libro.objects.all(), label='Libro')
    dias = forms.IntegerField(label='Días de préstamo', min_value=1, max_value=60, initial=14)