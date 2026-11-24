# ==================================================================
# ARCHIVO  : vet/admin.py
# PARTE 1  : VET (reserva de citas de la veterinaria)
# ROL      : DJANGO ADMIN -> personaliza /admin/ para Cita, Veterinario e Insumo.
# ------------------------------------------------------------------
# LAB 5        : aquí se creó (ModelAdmin, list_display, filtros e INLINES).
# LAB 7 - EJ 2 : sirve de APOYO para revisar los DATOS DE PRUEBA.
# NOTA     : no agrega modelos nuevos; el Admin REUTILIZA el Model y el ORM,
#            así que NO hace falta escribir views, urls ni templates.
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 7 - EJ 2 ..... línea 48
# ==================================================================

from django.contrib import admin

# Se importan los 5 modelos: 3 se registran como listados propios y los
# otros 2 (FichaClinica, ConsumoInsumo) solo se usan dentro de los Inlines.
from .models import Cita, ConsumoInsumo, FichaClinica, Insumo, Veterinario


# --- relacion 1:1 (Cita <-> FichaClinica) -------------------
# StackedInline: la ficha clinica se ve y edita dentro de la misma pantalla
# de la Cita a la que pertenece (maximo una, como corresponde al 1:1).
# Los campos salen uno debajo del otro, como un mini formulario.
class FichaClinicaInline(admin.StackedInline):
    # Modelo que se muestra "incrustado" dentro de la Cita.
    model = FichaClinica
    # extra = 0: no muestra un formulario vacio de mas; no toda cita tiene
    # ficha (solo las atendidas).
    extra = 0


# --- relacion N:M con modelo intermedio (Cita <-> Insumo) ---
# TabularInline: cada fila es un consumo de insumo, mostrando como columnas
# los atributos propios de la relacion (cantidad, precio_unitario).
# Se usa tabla porque una cita puede tener varios consumos.
class ConsumoInsumoInline(admin.TabularInline):
    # Se usa el modelo intermedio (through), no Insumo: asi se pueden
    # editar cantidad y precio_unitario de cada consumo.
    model = ConsumoInsumo
    # extra = 1: deja una fila vacia lista para agregar otro insumo.
    extra = 1


# --- ModelAdmin con list_display, search_fields y
# list_filter sobre la entidad principal (Cita), mas los dos Inlines -------
class CitaAdmin(admin.ModelAdmin):
    # Columnas del listado (en vez de solo el __str__ de cada cita).
    list_display = ('mascota', 'dueno', 'servicio', 'fecha', 'hora', 'estado', 'veterinario')
    # Caja de busqueda: busca por nombre de mascota o de dueno.
    search_fields = ('mascota', 'dueno')
    # Panel de filtros a la derecha: por estado, servicio y fecha.
    list_filter = ('estado', 'servicio', 'fecha')
    # Al abrir una cita aparecen debajo su ficha (1:1) y sus consumos (N:M).
    inlines = [FichaClinicaInline, ConsumoInsumoInline]


# --- segundo ModelAdmin personalizado, lado "1" de la FK -----
class VeterinarioAdmin(admin.ModelAdmin):
    # Columnas del listado de veterinarios.
    list_display = ('nombre', 'colegiatura', 'especialidad')
    # Busqueda por nombre o por numero de colegiatura.
    search_fields = ('nombre', 'colegiatura')


# --- registro de los modelos en el Admin ---------------------
# register(Modelo, ClaseAdmin) conecta cada modelo con su personalizacion.
# Insumo se registra sin clase: usa el listado generico de Django.
# FichaClinica y ConsumoInsumo NO se registran solos: solo tienen sentido
# dentro de una Cita, por eso se muestran como Inlines de CitaAdmin.
admin.site.register(Cita, CitaAdmin)
admin.site.register(Veterinario, VeterinarioAdmin)
admin.site.register(Insumo)
