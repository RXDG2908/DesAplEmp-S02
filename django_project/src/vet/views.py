# vet/views.py
# La "V" de MVT: recibe el request y devuelve el response.
# Ya no usa una lista en memoria: consulta y guarda en SQLite con el ORM.

from django.shortcuts import redirect, render

from .forms import CitaForm
from .models import Cita


def cita_list(request):
    # READ: pide las citas a la base (ORM -> SELECT) y las manda al template.
    citas = Cita.objects.order_by('fecha', 'hora')
    return render(request, 'vet/cita_list.html', {'citas': citas})


def cita_crear(request):
    # CREATE: registra una cita nueva.
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            # Guarda en la base (ORM -> INSERT).
            Cita.objects.create(
                mascota=datos['mascota'],
                dueno=datos['dueno'],
                servicio=datos['servicio'],
                fecha=datos['fecha'],
                hora=datos['hora'],
            )
            # Despues de guardar, vuelve al listado.
            return redirect('vet:cita_list')
    else:
        form = CitaForm()
    # GET o formulario invalido: muestra el formulario.
    return render(request, 'vet/cita_form.html', {'form': form})
