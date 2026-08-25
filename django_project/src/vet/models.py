from datetime import date, time

# Esta App no usa base de datos: la lista `citas` de más abajo es la única
# fuente de datos, en memoria. No hay migraciones ni panel de administración.

SERVICIOS = ['Consulta', 'Vacunación', 'Cirugía', 'Baño']
ESTADOS = ['Pendiente', 'Confirmada', 'Atendida']


class Cita:
    """Cita de la veterinaria, sin persistencia en base de datos."""

    def __init__(self, mascota, dueno, servicio, fecha, hora,
                 estado='Pendiente'):
        self.mascota = mascota
        self.dueno = dueno
        self.servicio = servicio
        self.fecha = fecha
        self.hora = hora
        self.estado = estado

    def __str__(self):
        return f'{self.mascota} - {self.servicio} ({self.fecha} {self.hora})'


citas = [
    Cita('Firulais', 'Renzo León', 'Consulta', date(2026, 8, 26), time(9, 0),
         'Confirmada'),
    Cita('Michi', 'Ana Torres', 'Vacunación', date(2026, 8, 26), time(10, 30)),
    Cita('Rocky', 'Luis Pérez', 'Baño', date(2026, 8, 26), time(11, 0)),
    Cita('Nala', 'Carla Ruiz', 'Cirugía', date(2026, 8, 27), time(8, 0),
         'Confirmada'),
    Cita('Toby', 'Renzo León', 'Consulta', date(2026, 8, 27), time(15, 0)),
]
