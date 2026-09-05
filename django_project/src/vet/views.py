# vet/views.py
# La View recibe el request, decide qué hacer y devuelve un response. Ya no
# trabaja con una lista en memoria: consulta y guarda en SQLite mediante el
# ORM de Django (Cita.objects...), así los datos persisten entre reinicios.

from django.shortcuts import redirect, render

from .forms import CitaForm
from .models import Cita


def cita_list(request):
    """READ: lista las citas leyéndolas de la base de datos con el ORM.

    Cita -> objects (Manager) -> order_by() -> QuerySet -> Django ORM
    -> SELECT -> SQLite.
    """
    citas = Cita.objects.order_by('fecha', 'hora')
    return render(request, 'vet/cita_list.html', {'citas': citas})


def cita_crear(request):
    """CREATE: registra una cita nueva de forma persistente con el ORM."""
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            # Cita.objects.create(...) -> Django ORM -> INSERT -> SQLite.
            # El registro queda guardado: sigue ahí tras reiniciar el servidor.
            Cita.objects.create(
                mascota=datos['mascota'],
                dueno=datos['dueno'],
                servicio=datos['servicio'],
                fecha=datos['fecha'],
                hora=datos['hora'],
            )
            # Post/Redirect/Get: tras el POST se redirige al listado, que
            # vuelve a consultar la base y muestra la cita recién creada.
            return redirect('vet:cita_list')
    else:
        form = CitaForm()
    return render(request, 'vet/cita_form.html', {'form': form})
