# ==================================================================
# GUIA: ARCHIVO  vet/api_views.py  (vistas de la API: devuelven JSON y codigos HTTP)
# LAB     : 08 (API REST con DRF) - Parte 1, app vet
# EJERCICIO: Ej.4 vistas genericas / Ej.5 InsumoViewSet / Ej.6 codigos HTTP /
#           Ej.7 CitaViewSet anidado / Ej.8 search, ordering, ?estado= y @action proximas
# QUE HACE : expone Insumo (CRUD completo) y Cita (solo lectura) reutilizando CitaQuerySet del Lab 07.
# SE PRUEBA: /api/insumos/?search=jer&ordering=-stock - /api/citas/?estado=Pendiente - /api/citas/proximas/
# DOCS    : ../../../docs/guiones/GUION-Lab08-Parte1.md - ../../../docs/exposiciones/EXPOSICION_Lab08_Parte1.md
# ==================================================================
# vet/api_views.py
# Lab 08 - las Views de la API. Igual que ./views.py reciben el request,
# pero en lugar de renderizar un Template devuelven JSON con un codigo HTTP.
# Reutilizan el mismo Model, las mismas relaciones y el CitaQuerySet de la
# Lab 07.

from rest_framework import filters, generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cita, Insumo
from .serializers import CitaSerializer, InsumoSerializer


# --- Lab 08 Ej.4: vistas genericas (primera version) -------------------
# Quedan como referencia: en el Ej.5 se reemplazaron por el
# InsumoViewSet de abajo y ya no estan enlazadas en ./api_urls.py.
class InsumoListCreate(generics.ListCreateAPIView):
    """GET /api/insumos/ (lista) y POST /api/insumos/ (crear)."""
    queryset = Insumo.objects.order_by('nombre')
    serializer_class = InsumoSerializer


class InsumoDetail(generics.RetrieveUpdateDestroyAPIView):
    """GET, PUT, PATCH y DELETE de /api/insumos/<pk>/."""
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer


# --- Lab 08 Ej.5 y 8: recurso simple con ModelViewSet -------------------
class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.order_by('nombre')
    serializer_class = InsumoSerializer
    # Lab 08 Ej.8 - ?search=texto y ?ordering=campo (o -campo).
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'unidad']
    ordering_fields = ['nombre', 'stock']


# --- Lab 08 Ej.7 y 8: recurso con relaciones, solo lectura -------------
class CitaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CitaSerializer

    def get_queryset(self):
        # select_related: veterinario (FK) y ficha (1:1) con JOIN.
        # prefetch_related: consumos y su insumo, en dos consultas extra.
        citas = (Cita.objects
                 .select_related('veterinario', 'ficha')
                 .prefetch_related('consumos__insumo')
                 .order_by('fecha', 'hora'))
        # Lab 08 Ej.8 - filtro por parametro: /api/citas/?estado=Pendiente
        estado = self.request.query_params.get('estado')
        if estado:
            citas = citas.con_estado(estado)
        return citas

    # Lab 08 Ej.8 - accion propia: GET /api/citas/proximas/
    # Reutiliza CitaQuerySet.proximas() del Lab 07 sobre el queryset ya
    # optimizado (y filtrado por ?estado= si se envio).
    @action(detail=False)
    def proximas(self, request):
        citas = self.get_queryset().proximas()
        serializer = self.get_serializer(citas, many=True)
        return Response(serializer.data)
