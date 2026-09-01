from django import forms

from .models import Cita


class CitaForm(forms.Form):
    """Formulario para registrar una nueva cita de la veterinaria."""

    # Las opciones salen del catálogo del modelo (Cita.SERVICIOS): no se
    # repiten aquí para no tener la misma lista en dos sitios.
    mascota = forms.CharField(label='Mascota', max_length=100)
    dueno = forms.CharField(label='Dueño', max_length=100)
    servicio = forms.ChoiceField(label='Servicio', choices=Cita.SERVICIOS)
    fecha = forms.DateField(
        label='Fecha',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    hora = forms.TimeField(
        label='Hora',
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )

    def clean(self):
        """Evita que dos citas queden agendadas en el mismo horario."""
        datos = super().clean()
        fecha = datos.get('fecha')
        hora = datos.get('hora')

        if fecha and hora:
            ocupado = Cita.objects.filter(fecha=fecha, hora=hora).exists()
            if ocupado:
                raise forms.ValidationError(
                    'Ya existe una cita agendada para esa fecha y hora.'
                )

        return datos
