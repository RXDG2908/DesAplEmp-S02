# vet/admin.py
# Laboratorio 5 - Django Admin.
# No se agregan modelos nuevos: se registra y personaliza en el Admin lo ya
# implementado en la Semana 4 (Cita, Veterinario, Insumo y sus 3 relaciones).

from django.contrib import admin

from .models import Cita, ConsumoInsumo, FichaClinica, Insumo, Veterinario


# --- Ejercicio 6: relacion 1:1 (Cita <-> FichaClinica) -------------------
# StackedInline: la ficha clinica se ve y edita dentro de la misma pantalla
# de la Cita a la que pertenece (maximo una, como corresponde al 1:1).
class FichaClinicaInline(admin.StackedInline):
    model = FichaClinica
    extra = 0


# --- Ejercicio 7: relacion N:M con modelo intermedio (Cita <-> Insumo) ---
# TabularInline: cada fila es un consumo de insumo, mostrando como columnas
# los atributos propios de la relacion (cantidad, precio_unitario).
class ConsumoInsumoInline(admin.TabularInline):
    model = ConsumoInsumo
    extra = 1


# --- Ejercicio 4 y 5: ModelAdmin con list_display, search_fields y
# list_filter sobre la entidad principal (Cita), mas los dos Inlines -------
class CitaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'dueno', 'servicio', 'fecha', 'hora', 'estado', 'veterinario')
    search_fields = ('mascota', 'dueno')
    list_filter = ('estado', 'servicio', 'fecha')
    inlines = [FichaClinicaInline, ConsumoInsumoInline]


# --- Ejercicio 4: segundo ModelAdmin personalizado, lado "1" de la FK -----
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'colegiatura', 'especialidad')
    search_fields = ('nombre', 'colegiatura')


# --- Ejercicio 3: registro simple del resto de entidades ------------------
admin.site.register(Cita, CitaAdmin)
admin.site.register(Veterinario, VeterinarioAdmin)
admin.site.register(Insumo)
