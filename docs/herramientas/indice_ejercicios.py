"""Uso (desde la raíz del repo):  python docs/herramientas/indice_ejercicios.py
Volver a correrlo después de editar código, porque los números de línea cambian.

Agrega a la cabecera de cada archivo un ÍNDICE con la línea donde está cada ejercicio.

Las líneas salen de:
  1) las marcas 'LAB X - EJ Y' que ya están DENTRO del código, y
  2) ANCLAS (texto que identifica el código del ejercicio) para los ejercicios
     que solo aparecían en la cabecera.
Es idempotente: si el índice ya existe, lo reemplaza con las líneas recalculadas.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
from inventario import archivos, cabecera, R

LUCAS = ('biblioteca', 'practica_lucas', 'Libro', 'Socio', 'Prestamo', 'datosBiblioteca', '_bib',
         'templates/biblioteca', 'components/Panel.jsx')
MARCA = re.compile(r"LAB ?(\d+) ?- ?EJ ?(\d+(?:\s*(?:,|y|-)\s*\d+)*)")
TITULO = "DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):"

# archivo -> {'LAB-EJ': texto del código que lo identifica}
ANCLAS = {
    "cargar_chamba.py": {"12-9": r"bulk_create"},
    "cargar_lab07.py": {"7-2": r"Veterinario\.objects\.get_or_create"},
    "medir_api_n1.py": {"8-7": r"CaptureQueriesContext\(connection\)"},
    "medir_n1.py": {"7-8": r"^reset_queries\(\)"},
    "catalogo/apps.py": {"13-6": r"^class "},
    "pedidos/apps.py": {"13-6": r"^class "},
    "servicios/apps.py": {"13-12": r"^class "},
    "clientes/apps.py": {"13-12": r"^class "},
    "solicitudes/apps.py": {"13-12": r"^class "},
    "catalogo/models.py": {"13-6": r"^from django"},
    "pedidos/models.py": {"13-6": r"^from django"},
    "servicios/models.py": {"13-12": r"^from django"},
    "clientes/models.py": {"13-12": r"^from django"},
    "solicitudes/models.py": {"13-12": r"^from django"},
    "chamba/api_urls.py": {"12-9": r"router\.register"},
    "chamba/api_views.py": {"12-9": r"^class PrestadorViewSet", "12-13": r"query_params\.get\('estado'\)"},
    "chamba/models.py": {"12-9": r"^class Prestador"},
    "chamba/serializers.py": {"12-11": r"raise serializers\.ValidationError"},
    "config/urls.py": {"8-4": r"path\('api/', include\('vet\.api_urls'\)\)"},
    "templates/base.html": {"7-3": r"consumo_registrar", "7-6": r"vet:reporte"},
    "vet/cita_detalle.html": {"7-3": r"Insumos utilizados", "7-8": r"cita\.consumos\.all"},
    "vet/cita_list.html": {"7-7": r"\{% for cita in citas %\}"},
    "vet/consumo_form.html": {"7-3": r"<form method"},
    "vet/reporte.html": {"7-4": r"Total global consumido", "7-5": r"Consumos por cita",
                         "7-6": r"\{% extends", "7-7": r"Citas próximas pendientes"},
    "vet/admin.py": {"7-2": r"^class CitaAdmin"},
    "vet/api_views.py": {"8-6": r"^class InsumoViewSet"},
    "frontend/src/api.js": {"12-3": r"axios\.create", "12-6": r"export function textoError",
                            "13-7": r"^const api ="},
    "frontend/src/App.jsx": {"9-4": r"multaPorDia \* diasAtraso", "11-1": r"<Practica />",
                             "11-10": r"<PanelCitas />", "11-11": r"<PanelPrestadores />",
                             "11-12": r"<PanelPrestadores />", "11-13": r"<PanelPrestadores />",
                             "12-4": r"<ListaPractica />"},
    "frontend/src/datos.js": {"9-5": r"^export const insumos", "9-7": r"^export const citas ="},
    "frontend/src/main.jsx": {"9-3": r"createRoot"},
    "frontend/src/Vet.jsx": {"9-4": r"precioConsulta \* \(1 \+ igv\)", "9-5": r"<InsumoLista",
                             "9-6": r"<InsumoLista", "10-1": r"^function Vet"},
    "components/Aviso.jsx": {"11-13": r"setTimeout"},
    "components/BuscadorCitas.jsx": {"11-13": r"<input"},
    "components/BuscadorPrestadores.jsx": {"11-13": r"<input", "12-13": r"onChange="},
    "components/CitaCard.jsx": {"10-4": r"<Tarjeta"},
    "components/CitaFila.jsx": {"11-10": r"<tr>", "11-11": r"onConfirmar\(cita\.id\)"},
    "components/CitaForm.jsx": {"11-12": r"function manejarEnvio"},
    "components/CitaListado.jsx": {"11-10": r"citas\.map", "11-13": r"No hay citas"},
    "components/ConsumoItem.jsx": {"10-5": r"^function ConsumoItem"},
    "components/FiltroEstadoPrestador.jsx": {"12-13": r"<select"},
    "components/InsumoCard.jsx": {"9-6": r"stock === 0 \?", "10-2": r"^function InsumoCard",
                                  "10-3": r"^function InsumoCard"},
    "components/InsumoLista.jsx": {"10-3": r"<InsumoCard key"},
    "components/PanelCitas.jsx": {"11-10": r"useState\(citasPanel\)"},
    "components/PanelPrestadores.jsx": {"11-10": r"const \[prestadores, setPrestadores\]",
                                        "11-12": r"async function guardarPrestador",
                                        "12-13": r"params: \{ search"},
    "components/PrestadorFila.jsx": {"11-10": r"<tr>", "11-11": r"'Aprobado'\)",
                                     "12-11": r"onEditar\(prestador\)", "12-12": r"confirmando \?"},
    "components/PrestadorForm.jsx": {"11-12": r"form\.nombres\.trim\(\) === ''",
                                     "12-11": r"await onGuardar"},
    "components/PrestadorListado.jsx": {"11-10": r"prestadores\.map", "11-13": r"No hay prestadores",
                                        "12-12": r"confirmando="},
    "components/ResumenCitas.jsx": {"11-13": r"const pendientes"},
    "components/ResumenPrestadores.jsx": {"11-13": r"const aprobados", "12-13": r"\.reduce\("},
    "components/Tarjeta.jsx": {"10-4": r"\{children\}"},
    "practica/Buscador.jsx": {"11-7": r"<input"},
    "practica/Carrito.jsx": {"11-4": r"lineas\.map", "11-6": r"onQuitar\(l\.id\)"},
    "practica/Catalogo.jsx": {"11-1": r"productos\.map", "11-3": r"onAgregar=\{onAgregar\}",
                              "11-7": r"No hay productos"},
    "practica/datos.js": {"11-1": r"^export const productos"},
    "practica/ListaPractica.jsx": {"12-4": r"api\.get\(", "12-5": r"\} finally \{", "12-6": r"api\.post\(",
                                   "12-7": r"api\.delete\(", "12-8": r"params: \{ search"},
    "practica/Practica.jsx": {"11-1": r"<Catalogo ", "11-3": r"function agregarAlCarrito", "11-8": r"<Aviso "},
    "practica/ProductoCard.jsx": {"11-1": r"toFixed\(2\)", "11-2": r"^function ProductoCard",
                                  "11-3": r"onClick="},
}

# Para la marca "LAB 8 - EJ 4 y 5" del encabezado de config/urls.py
ALIAS_CABECERA = {}


def expandir(ejs):
    """'4 y 5' -> [4, 5]; '4, 5 y 6' -> [4,5,6]; '10-13' -> [10..13]."""
    ejs = ejs.replace(" ", "")
    if "-" in ejs and "," not in ejs and "y" not in ejs:
        a, b = ejs.split("-")
        return list(range(int(a), int(b) + 1))
    return [int(x) for x in re.split(r"[,y]", ejs) if x]


def comentario(ext):
    if ext == ".html":
        return lambda s: "{# " + s + " #}"
    if ext in (".js", ".jsx", ".css"):
        return lambda s: "// " + s
    return lambda s: "# " + s


def procesar(p):
    rel = os.path.relpath(p, R).replace("\\", "/")
    crudo = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in crudo else "\n"
    lineas = crudo.replace("\r\n", "\n").split("\n")
    h = cabecera(lineas)
    if h == 0:
        return None
    cab, cuerpo = lineas[:h], lineas[h:]
    # quitar un índice anterior
    if any(TITULO in l for l in cab):
        i = next(k for k, l in enumerate(cab) if TITULO in l)
        if i > 0 and '-----' in cab[i - 1]:
            i -= 1
            j0 = i + 2
        else:
            j0 = i + 1
        j = j0
        while j < len(cab) and re.search(r"LAB \d+ - EJ \d+\s*\.+", cab[j]):
            j += 1
        cab = cab[:i] + cab[j:]
    # ejercicios citados en la cabecera
    en_cab = set()
    for l in cab:
        for lab, ejs in MARCA.findall(l):
            for e in expandir(ejs):
                en_cab.add((int(lab), e))
    if not en_cab:
        return None
    # líneas: marcas dentro del código
    donde = {}
    for k, l in enumerate(cuerpo):
        for lab, ejs in MARCA.findall(l):
            for e in expandir(ejs):
                donde.setdefault((int(lab), e), []).append(k)
    # anclas
    anclas = next((v for clave, v in ANCLAS.items() if rel.endswith(clave)), {})
    for clave, patron in anclas.items():
        lab, e = map(int, clave.split("-"))
        if (lab, e) in donde:
            continue
        k = next((k for k, l in enumerate(cuerpo) if re.search(patron, l)), None)
        if k is None:
            print("  !! ancla sin coincidencia:", rel, clave, patron)
            continue
        donde.setdefault((lab, e), []).append(k)
    faltan = sorted(t for t in en_cab if t not in donde)
    entradas = sorted(t for t in en_cab if t in donde)
    if not entradas:
        if faltan:
            print("  -- sin código para indexar:", rel, faltan)
        return None
    c = comentario(os.path.splitext(p)[1])
    fin = max(k for k, l in enumerate(cab) if "=====" in l)
    n_indice = 1 + len(entradas)
    total_cab = len(cab) + n_indice
    nuevas = [c(TITULO)]
    for lab, e in entradas:
        nums = sorted({total_cab + k + 1 for k in donde[(lab, e)]})
        etiqueta = f"LAB {lab} - EJ {e} "
        lin = ("línea " if len(nums) == 1 else "líneas ") + ", ".join(map(str, nums))
        nuevas.append(c(f"  {etiqueta.ljust(18, '.')} {lin}"))
    sep = [l for l in cab if "-----" in l]
    bloque = ([sep[0]] if sep else []) + nuevas
    cab2 = cab[:fin] + bloque + cab[fin:]
    # recalcular con el tamaño real (por si se agregó el separador)
    ajuste = len(cab2) - total_cab
    if ajuste:
        nuevas2 = [bloque[0]] if sep else []
        nuevas2.append(c(TITULO))
        for lab, e in entradas:
            nums = sorted({len(cab2) + k + 1 for k in donde[(lab, e)]})
            etiqueta = f"LAB {lab} - EJ {e} "
            lin = ("línea " if len(nums) == 1 else "líneas ") + ", ".join(map(str, nums))
            nuevas2.append(c(f"  {etiqueta.ljust(18, '.')} {lin}"))
        cab2 = cab[:fin] + nuevas2 + cab[fin:]
    texto = nl.join(cab2 + cuerpo)
    open(p, "w", encoding="utf-8", newline="").write(texto)
    if faltan:
        print("  -- sin línea:", rel, faltan)
    return rel, len(entradas)


if __name__ == "__main__":
    n = 0
    for p in archivos():
        rel = os.path.relpath(p, R).replace("\\", "/")
        if any(k in rel for k in LUCAS):
            continue
        r = procesar(p)
        if r:
            n += 1
            print(f"{r[1]:3} ejercicios  {r[0]}")
    print(n, "archivos con índice")
