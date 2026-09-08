# vet/forms.py
# El formulario: define que datos se piden y como se validan.

from django import forms

from .models import Cita


class CitaForm(forms.Form):
    # Se usa forms.Form (no ModelForm), como en el material.

    # Campos que ve el usuario.
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

    # Validacion extra: no permitir dos citas en el mismo horario.
    def clean(self):
        datos = super().clean()
        fecha = datos.get('fecha')
        hora = datos.get('hora')

        if fecha and hora:
            # Consulta la base con el ORM.
            ocupado = Cita.objects.filter(fecha=fecha, hora=hora)
            if ocupado:
                raise forms.ValidationError(
                    'Ya existe una cita agendada para esa fecha y hora.'
                )

        return datos
