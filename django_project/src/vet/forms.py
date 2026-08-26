from django import forms

from .models import SERVICIOS, citas


class CitaForm(forms.Form):
    """Formulario para registrar una nueva cita de la veterinaria."""

    mascota = forms.CharField(label='Mascota', max_length=100)
    dueno = forms.CharField(label='Dueño', max_length=100)
    servicio = forms.ChoiceField(
        label='Servicio',
        choices=[(servicio, servicio) for servicio in SERVICIOS],
    )
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
            ocupado = any(c.fecha == fecha and c.hora == hora for c in citas)
            if ocupado:
                raise forms.ValidationError(
                    'Ya existe una cita agendada para esa fecha y hora.'
                )

        return datos
