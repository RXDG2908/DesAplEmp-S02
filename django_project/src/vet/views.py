# vet/views.py
# La "V" de MVT: recibe el request y devuelve el response.
# Semana 4: las consultas ahora recorren relaciones con select_related()
# y prefetch_related().

from django.db import transaction
from django.db.models import Count, DecimalField, F, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CitaForm, ConsumoForm
from .models import Cita, ConsumoInsumo, Insumo


def cita_list(request):
    # Ejercicio 6 - select_related(): resuelve la FK (1:N) y el 1:1 inverso
    # en UNA sola consulta con JOIN, en vez de una consulta extra por fila.
    citas = (Cita.objects
             .select_related('veterinario', 'ficha')
             .order_by('fecha', 'hora'))
    estado = request.GET.get('estado')
    if estado:
        citas = citas.con_estado(estado)
    return render(request, 'vet/cita_list.html', {'citas': citas})


def cita_detalle(request, pk):
    # Ejercicio 6 - prefetch_related(): recorre el modelo intermedio.
    # Django lanza una consulta extra para los ConsumoInsumo y otra para los
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


def cita_crear(request):
    # CREATE: registra una cita nueva.
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

def consumo_registrar(request):
    error = None
    if request.method == 'POST':
        form = ConsumoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            try:
                with transaction.atomic():
                    ConsumoInsumo.objects.create(
                        cita=datos['cita'],
                        insumo=datos['insumo'],
                        cantidad=datos['cantidad'],
                        precio_unitario=datos['precio_unitario'],
                    )
                    Cita.objects.filter(pk=datos['cita'].pk).update(estado='Atendida')
                    filas = Insumo.objects.filter(
                        pk=datos['insumo'].pk,
                        stock__gte=datos['cantidad'],
                    ).update(stock=F('stock') - datos['cantidad'])
                    if filas == 0:
                        raise ValueError('Stock insuficiente de ' + datos['insumo'].nombre)
            except ValueError as e:
                error = str(e)
            else:
                return redirect('vet:cita_detalle', pk=datos['cita'].pk)
    else:
        form = ConsumoForm()
    return render(request, 'vet/consumo_form.html', {'form': form, 'error': error})

def reporte(request):
    total = ConsumoInsumo.objects.aggregate(
        total=Sum(F('cantidad') * F('precio_unitario'), output_field=DecimalField())
    )['total']
    por_cita = Cita.objects.annotate(n=Count('consumos')).order_by('-n')
    por_estado = Cita.objects.values('estado').annotate(total=Count('id')).order_by('-total')
    pendientes_proximas = Cita.objects.proximas().con_estado('Pendiente').count()
    return render(request, 'vet/reporte.html', {
        'total': total,
        'por_cita': por_cita,
        'por_estado': por_estado,
        'pendientes_proximas': pendientes_proximas,
    })