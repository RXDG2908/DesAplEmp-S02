from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import CitaForm
from .models import Cita


def cita_list(request):
    """Obtiene las citas desde SQLite mediante un QuerySet (ORM)."""
    citas_ordenadas = Cita.objects.all().order_by('fecha', 'hora')
    return render(request, 'vet/cita_list.html', {'citas': citas_ordenadas})


def cita_crear(request):
    """Muestra el formulario y, en POST válido, guarda la cita en SQLite."""
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
            messages.success(
                request,
                'Cita registrada de forma persistente en la base de datos.',
            )
            return redirect('vet:cita_list')
    else:
        form = CitaForm()
    return render(request, 'vet/cita_form.html', {'form': form})