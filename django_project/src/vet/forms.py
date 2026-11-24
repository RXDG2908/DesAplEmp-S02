# ==================================================================
# ARCHIVO  : vet/forms.py
# PARTE 1  : VET (reserva de citas de la veterinaria)
# ROL      : FORMULARIOS -> definen QUÉ DATOS se piden y CÓMO SE VALIDAN.
# ------------------------------------------------------------------
# LAB 7 - EJ 3: ConsumoForm -> pide cita, insumo, cantidad (>= 1) y precio
#               para la TRANSACCIÓN de consumo_registrar.
# NOTA     : CitaForm ya existía (Lab 2-3); evita DOS CITAS en el mismo horario.
# ------------------------------------------------------------------
# USADO EN : ./views.py (cita_crear y consumo_registrar)
# DOCS     : ../../../docs/guiones/GUION-Lab07-Parte1.md
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 7 - EJ 3 ..... línea 54
# ==================================================================

from django import forms

from .models import Cita, Insumo


class CitaForm(forms.Form):
    # Se usa forms.Form (NO ModelForm), como en el material del curso.

    # CAMPOS que ve el usuario.
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

    # VALIDACIÓN EXTRA: no permitir DOS CITAS en la misma fecha y hora.
    def clean(self):
        datos = super().clean()
        fecha = datos.get('fecha')
        hora = datos.get('hora')

        if fecha and hora:
            # CONSULTA la base de datos con el ORM.
            ocupado = Cita.objects.filter(fecha=fecha, hora=hora)
            if ocupado:
                raise forms.ValidationError(
                    'Ya existe una cita agendada para esa fecha y hora.'
                )

        return datos

# --- LAB 7 - EJ 3: FORMULARIO de la pantalla 'Registrar consumo' ----------
# Lo PROCESA ./views.py -> consumo_registrar y lo DIBUJA ../templates/vet/consumo_form.html.
# min_value=1 en cantidad: no se puede registrar un consumo de CERO unidades.
class ConsumoForm(forms.Form):
    cita = forms.ModelChoiceField(queryset=Cita.objects.all(), label='Cita')
    insumo = forms.ModelChoiceField(queryset=Insumo.objects.all(), label='Insumo')
    cantidad = forms.IntegerField(label='Cantidad', min_value=1)
    precio_unitario = forms.DecimalField(label='Precio unitario', min_value=0, max_digits=7, decimal_places=2)