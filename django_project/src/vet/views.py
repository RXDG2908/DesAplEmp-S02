from django.shortcuts import render

from .models import citas


def cita_list(request):
    """Ordena las citas de la lista en memoria y las envía a la plantilla."""
    citas_ordenadas = sorted(citas, key=lambda c: (c.fecha, c.hora))
    return render(request, 'vet/cita_list.html', {'citas': citas_ordenadas})
