# ==================================================================
# ARCHIVO  : vet/api_views.py
# PARTE 1  : VET (reserva de citas de la veterinaria)
# ROL      : VISTAS DE LA API. Igual que ./views.py reciben el REQUEST, pero en
#            lugar de renderizar un Template devuelven JSON + CÓDIGO HTTP.
#            Reutilizan el mismo Model y el CitaQuerySet del Lab 7.
# ------------------------------------------------------------------
# LAB 8 - EJ 4: InsumoListCreate / InsumoDetail -> VISTAS GENÉRICAS (1.ª versión).
# LAB 8 - EJ 5: InsumoViewSet -> MODELVIEWSET que reemplaza a las genéricas.
# LAB 8 - EJ 6: CRUD probado con CÓDIGOS HTTP 200, 201, 400, 404 y 204.
# LAB 8 - EJ 7: CitaViewSet -> SOLO LECTURA con relaciones ANIDADAS y sin N+1.
# LAB 8 - EJ 8: ?search=, ?ordering=, ?estado= y la ACCIÓN PROPIA /proximas/.
# ------------------------------------------------------------------
# SE PRUEBA: /api/insumos/?search=jer&ordering=-stock
#            /api/citas/?estado=Pendiente  ·  /api/citas/proximas/
# DOCS     : ../../../docs/guiones/GUION-Lab08-Parte1.md
#            ../../../docs/exposiciones/EXPOSICION_Lab08_Parte1.md
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 8 - EJ 4 ..... línea 35
#   LAB 8 - EJ 5 ..... línea 50
#   LAB 8 - EJ 6 ..... línea 51
#   LAB 8 - EJ 7 ..... líneas 60, 65
#   LAB 8 - EJ 8 ..... líneas 50, 54, 60, 72, 78
# ==================================================================

from rest_framework import filters, generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cita, Insumo
from .serializers import CitaSerializer, InsumoSerializer


# --- LAB 8 - EJ 4: VISTAS GENÉRICAS (primera versión) ------------------
# Quedan como REFERENCIA: en el EJ 5 se REEMPLAZARON por el InsumoViewSet
# de abajo y ya NO están enlazadas en ./api_urls.py.
class InsumoListCreate(generics.ListCreateAPIView):
    """GET /api/insumos/ (lista) y POST /api/insumos/ (crear)."""
    queryset = Insumo.objects.order_by('nombre')
    serializer_class = InsumoSerializer


class InsumoDetail(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH y DELETE de /api/insumos/<pk>/."""
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer


# --- LAB 8 - EJ 5 y 8: recurso SIMPLE con ModelViewSet (CRUD COMPLETO) ---
class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.order_by('nombre')
    serializer_class = InsumoSerializer
    # LAB 8 - EJ 8: BÚSQUEDA con ?search=texto y ORDEN con ?ordering=campo (o -campo).
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'unidad']
    ordering_fields = ['nombre', 'stock']


# --- LAB 8 - EJ 7 y 8: recurso CON RELACIONES, SOLO LECTURA ------------
class CitaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitaSerializer

    def get_queryset(self):
        # LAB 8 - EJ 7: QUERYSET OPTIMIZADO (de 24 a 3 consultas, ver ../medir_api_n1.py).
        # select_related: veterinario (FK) y ficha (1:1) con JOIN.
        # prefetch_related: consumos y su insumo, en DOS consultas extra.
        citas = (Cita.objects
                 .select_related('veterinario', 'ficha')
                 .prefetch_related('consumos__insumo')
                 .order_by('fecha', 'hora'))
        # LAB 8 - EJ 8: FILTRO POR PARÁMETRO -> /api/citas/?estado=Pendiente
        estado = self.request.query_params.get('estado')
        if estado:
            citas = citas.con_estado(estado)
        return citas

    # LAB 8 - EJ 8: ACCIÓN PROPIA -> GET /api/citas/proximas/
    # REUTILIZA CitaQuerySet.proximas() del Lab 7 sobre el queryset ya
    # optimizado (y filtrado por ?estado= si se envió).
    @action(detail=False)
    def proximas(self, request):
        citas = self.get_queryset().proximas()
        serializer = self.get_serializer(citas, many=True)
        return Response(serializer.data)
