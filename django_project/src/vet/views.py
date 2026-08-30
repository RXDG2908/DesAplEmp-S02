from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import CitaForm
from .models import Cita, citas


def cita_list(request):
    """Ordena las citas de la lista en memoria y las envía a la plantilla."""
    citas_ordenadas = sorted(citas, key=lambda c: (c.fecha, c.hora))
    return render(request, 'vet/cita_list.html', {'citas': citas_ordenadas})


def cita_crear(request):
    """Muestra el formulario y, en POST válido, agrega la cita a la lista."""
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            citas.append(Cita(
                mascota=datos['mascota'],
                dueno=datos['dueno'],
                servicio=datos['servicio'],
                fecha=datos['fecha'],
                hora=datos['hora'],
            ))
            messages.success(
                request,
                'Cita registrada. Se perderá al reiniciar el servidor.',
            )
            return redirect('vet:cita_list')
    else:
        form = CitaForm()
    return render(request, 'vet/cita_form.html', {'form': form})
