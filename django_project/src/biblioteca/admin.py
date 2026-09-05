from django.contrib import admin

from .models import Bibliotecario, Categoria, Editorial, Libro, Socio

admin.site.register(Bibliotecario)
admin.site.register(Editorial)
admin.site.register(Socio)
admin.site.register(Categoria)
admin.site.register(Libro)
