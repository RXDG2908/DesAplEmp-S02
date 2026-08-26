# Reserva de citas — Veterinaria (Laboratorio 02)

Aplicación Web en Django sin base de datos: gestiona citas de una veterinaria
usando datos estáticos en memoria. Curso: **Desarrollo de Aplicaciones
Empresariales** (4 - C24 - Sección CD). Trabajo en equipo de 2 integrantes.

## Problemática

Una veterinaria de barrio recibe las solicitudes de cita por llamada o
mensaje, sin ningún registro centralizado, lo que provoca citas encimadas y
olvidos. Esta app permite registrar y consultar citas (mascota, dueño,
servicio, fecha, hora y estado) desde una única lista en memoria — sin
migraciones ni panel de administración.

## Estructura del proyecto

```
django_project/
├── venv/                     # Entorno virtual de Python (no se sube a Git)
├── README.md
└── src/                      # Código fuente
    ├── manage.py
    ├── requirements.txt
    ├── config/                # Configuración del proyecto (Project)
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── vet/                   # App de reserva de citas (sin base de datos)
    │   ├── models.py          # Clase Cita + lista `citas` en memoria
    │   ├── views.py           # Vista cita_list (listado ordenado)
    │   ├── urls.py            # Ruta vet:cita_list
    │   ├── forms.py           # Formulario de registro de citas
    │   └── admin.py
    └── templates/
        ├── base.html
        └── vet/
            └── cita_list.html   # Listado de citas
```

## Modelo `Cita` (datos estáticos, sin base de datos)

| Campo      | Tipo                      | Descripción                                  |
|------------|---------------------------|-----------------------------------------------|
| `mascota`  | texto                     | Nombre de la mascota                          |
| `dueno`    | texto                     | Nombre del propietario, para contactarlo      |
| `servicio` | texto (opciones)          | Consulta, Vacunación, Cirugía, Baño           |
| `fecha`    | `date`                    | Día de la cita                                |
| `hora`     | `time`                    | Hora de la cita                               |
| `estado`   | texto (opciones)          | Pendiente, Confirmada, Atendida (default: Pendiente) |

## Instalación

Requisitos: Python 3.10 o superior.

```bash
git clone https://github.com/RXDG2908/DesAplEmp-S02.git
cd DesAplEmp-S02/django_project
python -m venv venv
venv\Scripts\activate          # En Linux/Mac: source venv/bin/activate
cd src
pip install -r requirements.txt
```

## Ejecución

```bash
python manage.py runserver
```

- Listado de citas: http://127.0.0.1:8000/

## Estado del laboratorio

- [x] Ejercicio 1 — Problemática
- [x] Ejercicio 2 — Requisitos funcionales
- [x] Ejercicio 3 — Diseño del modelo de datos
- [x] Ejercicio 4 — Crear la nueva App (`vet`)
- [x] Ejercicio 5 — Model con datos estáticos
- [x] Ejercicio 6 — Listado (View + URL + Template)
- [x] Ejercicio 7 — Formulario (Forms)
- [ ] Ejercicio 8 — Vista de creación
- [ ] Ejercicio 9 — Verificación del flujo completo
- [ ] Ejercicio 10 — Publicar en GitHub

## Autores

- Renzo León (RXDG2908)
