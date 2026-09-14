# vet/views.py
# La "V" de MVT: recibe el request y devuelve el response.
# Semana 4: las consultas ahora recorren relaciones con select_related()
# y prefetch_related().

from django.shortcuts import get_object_or_404, redirect, render

from .forms import CitaForm
from .models import Cita


def cita_list(request):
    # Ejercicio 6 - select_related(): resuelve la FK (1:N) y el 1:1 inverso
    # en UNA sola consulta con JOIN, en vez de una consulta extra por fila.
    citas = (Cita.objects
             .select_related('veterinario', 'ficha')
             .order_by('fecha', 'hora'))
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
