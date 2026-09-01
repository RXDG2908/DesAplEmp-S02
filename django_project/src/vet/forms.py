# vet/forms.py
# Un Form define QUÉ datos pide la aplicación al usuario y CÓMO se validan,
# antes de que la View los use. No dibuja HTML ni toca la base de datos: solo
# recibe lo que llega en el request.POST y dice si es válido.

from django import forms

from .models import Cita
# Se importa `Cita` para reutilizar su catálogo `Cita.SERVICIOS` y para
# consultar la tabla en la validación (no se vuelve a escribir la lista aquí).


class CitaForm(forms.Form):
    """Formulario para registrar una nueva cita de la veterinaria.

    Hereda de `forms.Form` (formulario "manual"): cada campo se declara a mano.
    Se usa esta variante, y no `ModelForm`, porque los campos coinciden con los
    de la Semana 2 y así se ve explícito qué se le pide al usuario.
    """

    # --- Campos del formulario ---------------------------------------
    # Cada atributo es un campo que se renderiza como <input>/<select>. El
    # `label` es el texto visible; `max_length` limita la entrada.
    mascota = forms.CharField(label='Mascota', max_length=100)
    dueno = forms.CharField(label='Dueño', max_length=100)
    # `ChoiceField` = desplegable. Las opciones salen de `Cita.SERVICIOS`:
    # una sola fuente de verdad, compartida con el modelo.
    servicio = forms.ChoiceField(label='Servicio', choices=Cita.SERVICIOS)
    # `widget=DateInput/TimeInput con type=date/time` hace que el navegador
    # muestre el selector nativo de fecha y de hora.
    fecha = forms.DateField(
        label='Fecha',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    hora = forms.TimeField(
        label='Hora',
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )

    # --- Validación propia -------------------------------------------
    # `clean()` corre después de validar cada campo por separado y sirve para
    # reglas que dependen de VARIOS campos a la vez (aquí: fecha + hora).
    def clean(self):
        """Evita que dos citas queden agendadas en el mismo horario."""
        datos = super().clean()          # datos ya limpios de cada campo
        fecha = datos.get('fecha')
        hora = datos.get('hora')

        if fecha and hora:
            # Se consulta la TABLA (ya no una lista en memoria): ¿existe alguna
            # cita con esa fecha y hora? `.exists()` devuelve True/False sin
            # traer el registro completo.
            ocupado = Cita.objects.filter(fecha=fecha, hora=hora).exists()
            if ocupado:
                # Lanzar ValidationError marca el formulario como no válido y
                # muestra el mensaje al usuario.
                raise forms.ValidationError(
                    'Ya existe una cita agendada para esa fecha y hora.'
                )

        return datos
