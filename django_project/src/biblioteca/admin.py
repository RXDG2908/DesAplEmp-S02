from django.contrib import admin

from .models import (
    Bibliotecario, CarnetSocio, Categoria, Editorial, Libro, Prestamo, Socio,
)


class CarnetSocioInline(admin.StackedInline):
    model = CarnetSocio
    extra = 0


class PrestamoInline(admin.TabularInline):
    model = Prestamo
    extra = 1


class SocioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dni', 'telefono')
    search_fields = ('nombre', 'dni')
    inlines = [CarnetSocioInline, PrestamoInline]


class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'anio_publicacion')
    search_fields = ('titulo', 'autor', 'isbn')
    list_filter = ('categoria',)


class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('socio', 'libro', 'fecha_prestamo',
                     'fecha_devolucion_prevista', 'estado')
    list_filter = ('estado',)


admin.site.register(Socio, SocioAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Prestamo, PrestamoAdmin)
admin.site.register(Bibliotecario)
admin.site.register(Editorial)
admin.site.register(Categoria)