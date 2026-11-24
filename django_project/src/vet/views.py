# ==================================================================
# ARCHIVO  : vet/views.py
# PARTE 1  : VET (reserva de citas de la veterinaria)
# ROL      : la "V" de MVT -> recibe el REQUEST y devuelve el RESPONSE (HTML).
# ------------------------------------------------------------------
# LAB 7 - EJ 3: consumo_registrar -> TRANSACCIÓN con transaction.atomic() + F().
# LAB 7 - EJ 4: reporte -> TOTAL GLOBAL con aggregate().
# LAB 7 - EJ 5: reporte -> VALORES POR OBJETO con annotate() y values().annotate().
# LAB 7 - EJ 6: reporte -> PÁGINA DE REPORTE (../templates/vet/reporte.html).
# LAB 7 - EJ 7: cita_list y reporte USAN el QuerySet propio (con_estado, proximas).
# LAB 7 - EJ 8: cita_list y cita_detalle EVITAN el N+1 con select_related()
#               y prefetch_related().
# NOTA     : cita_list, cita_detalle y cita_crear ya existían; lo NUEVO del
#            Lab 7 es consumo_registrar y reporte.
# ------------------------------------------------------------------
# SE PRUEBA: /  ·  /?estado=Pendiente  ·  /cita/<id>/  ·  /consumo/nuevo/  ·  /reporte/
# DOCS     : ../../../docs/guiones/GUION-Lab07-Parte1.md
#            ../../../docs/exposiciones/EXPOSICION_Lab07_Parte1.md
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 7 - EJ 3 ..... líneas 85, 97, 106, 112
#   LAB 7 - EJ 4 ..... líneas 123, 128
#   LAB 7 - EJ 5 ..... líneas 123, 132
#   LAB 7 - EJ 6 ..... línea 123
#   LAB 7 - EJ 7 ..... líneas 37, 135
#   LAB 7 - EJ 8 ..... líneas 39, 50, 52
# ==================================================================

from django.db import transaction
from django.db.models import Count, DecimalField, F, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CitaForm, ConsumoForm
from .models import Cita, ConsumoInsumo, Insumo


# LAB 7 - EJ 7: LISTADO de citas; el filtro ?estado= usa con_estado() del QuerySet.
def cita_list(request):
    # LAB 7 - EJ 8: select_related() resuelve la FK (1:N) y el 1:1 inverso
    # en UNA SOLA CONSULTA con JOIN, en vez de una consulta extra por fila (N+1).
    citas = (Cita.objects
             .select_related('veterinario', 'ficha')
             .order_by('fecha', 'hora'))
    estado = request.GET.get('estado')
    if estado:
        citas = citas.con_estado(estado)
    return render(request, 'vet/cita_list.html', {'citas': citas})


# LAB 7 - EJ 8: DETALLE con veterinario, ficha y consumos SIN N+1.
def cita_detalle(request, pk):
    # LAB 7 - EJ 8: prefetch_related() recorre el MODELO INTERMEDIO.
    # Django lanza UNA consulta extra para los ConsumoInsumo y OTRA para los
    # Insumo, y une los resultados en Python.
    cita = get_object_or_404(
        Cita.objects
            .select_related('veterinario', 'ficha')
            .prefetch_related('consumos__insumo'),
        pk=pk,
    )
    total = sum(c.subtotal for c in cita.consumos.all())
    return render(request, 'vet/cita_detalle.html',
                  {'cita': cita, 'total': total})


# FORMULARIO para registrar una cita (patrón POST/REDIRECT/GET).
def cita_crear(request):
    # CREATE: registra una cita nueva con el ORM.
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            Cita.objects.create(
                mascota=datos['mascota'],
                dueno=datos['dueno'],
                servicio=datos['servicio'],
                fecha=datos['fecha'],
                hora=datos['hora'],
            )
            return redirect('vet:cita_list')
    else:
        form = CitaForm()
    return render(request, 'vet/cita_form.html', {'form': form})

# --- LAB 7 - EJ 3: TRANSACCIÓN con transaction.atomic() + F() -------------
# Registrar un consumo toca 3 MODELOS y debe ser TODO O NADA:
#   1) CREA el ConsumoInsumo   2) marca la Cita como 'Atendida'   3) DESCUENTA el stock.
# Si falta stock se lanza ValueError y atomic() DESHACE también los pasos 1 y 2 (ROLLBACK).
# Plantilla: ../templates/vet/consumo_form.html  ·  Ruta: /consumo/nuevo/
def consumo_registrar(request):
    error = None
    if request.method == 'POST':
        form = ConsumoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            try:
                # LAB 7 - EJ 3: todo este bloque se CONFIRMA junto o se DESHACE junto.
                with transaction.atomic():
                    ConsumoInsumo.objects.create(
                        cita=datos['cita'],
                        insumo=datos['insumo'],
                        cantidad=datos['cantidad'],
                        precio_unitario=datos['precio_unitario'],
                    )
                    Cita.objects.filter(pk=datos['cita'].pk).update(estado='Atendida')
                    # LAB 7 - EJ 3: F('stock') - cantidad hace la RESTA DENTRO DE LA BASE DE DATOS
                    # (dos registros simultáneos no se pisan); stock__gte evita descontar más de lo que hay.
                    filas = Insumo.objects.filter(
                        pk=datos['insumo'].pk,
                        stock__gte=datos['cantidad'],
                    ).update(stock=F('stock') - datos['cantidad'])
                    # LAB 7 - EJ 3: 0 filas actualizadas = NO ALCANZÓ EL STOCK -> ValueError -> ROLLBACK.
                    if filas == 0:
                        raise ValueError('Stock insuficiente de ' + datos['insumo'].nombre)
            except ValueError as e:
                error = str(e)
            else:
                return redirect('vet:cita_detalle', pk=datos['cita'].pk)
    else:
        form = ConsumoForm()
    return render(request, 'vet/consumo_form.html', {'form': form, 'error': error})

# --- LAB 7 - EJ 4, 5 y 6: aggregate() y annotate() en la PÁGINA DE REPORTE ---
# aggregate() -> UN SOLO VALOR para toda la tabla (devuelve un DICCIONARIO, no un QuerySet).
# annotate()  -> un valor POR CADA OBJETO o grupo (sigue siendo un QuerySet).
# Plantilla: ../templates/vet/reporte.html  ·  Ruta: /reporte/
def reporte(request):
    # LAB 7 - EJ 4: TOTAL GLOBAL consumido = suma de cantidad × precio_unitario.
    total = ConsumoInsumo.objects.aggregate(
        total=Sum(F('cantidad') * F('precio_unitario'), output_field=DecimalField())
    )['total']
    # LAB 7 - EJ 5: NÚMERO DE CONSUMOS por cita y CITAS AGRUPADAS POR ESTADO.
    por_cita = Cita.objects.annotate(n=Count('consumos')).order_by('-n')
    por_estado = Cita.objects.values('estado').annotate(total=Count('id')).order_by('-total')
    # LAB 7 - EJ 7: métodos del QuerySet propio ENCADENADOS.
    pendientes_proximas = Cita.objects.proximas().con_estado('Pendiente').count()
    return render(request, 'vet/reporte.html', {
        'total': total,
        'por_cita': por_cita,
        'por_estado': por_estado,
        'pendientes_proximas': pendientes_proximas,
    })