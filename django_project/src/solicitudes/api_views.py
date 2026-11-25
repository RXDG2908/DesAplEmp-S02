# ==================================================================
# ARCHIVO  : solicitudes/api_views.py
# PROYECTO : CHAMBA PE (proyecto integrador)
# ROL      : CONTROLADOR de la solicitud de servicio: CRUD, búsqueda, filtro y avance de estado.
# ------------------------------------------------------------------
# LAB 14 - EJ 11: SolicitudViewSet (ModelViewSet) con SearchFilter. Al CREAR, dentro de
#                 transaction.atomic: el MONTO se toma de la tarifa del prestador en la BD
#                 y se registra el primer SEGUIMIENTO (Pendiente).
# LAB 14 - EJ 11: acción /avanzar/ -> los estados avanzan SOLO en orden y cada cambio
#                 queda en SeguimientoSolicitud.
# ------------------------------------------------------------------
# USADO EN : ./api_urls.py
# SE PRUEBA: /api/solicitudes/?search=rosa  ·  /api/solicitudes/?estado=PEN
#            POST /api/solicitudes/<id>/avanzar/
# ------------------------------------------------------------------
# DÓNDE ESTÁ CADA EJERCICIO (número de línea en este archivo):
#   LAB 14 - EJ 11 ... líneas 43, 52
# ==================================================================
from django.db import transaction
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import SeguimientoSolicitud, Solicitud
from .serializers import SolicitudSerializer


class SolicitudViewSet(viewsets.ModelViewSet):
    serializer_class = SolicitudSerializer
    filter_backends = [filters.SearchFilter]
    # ?search= busca por cliente, prestador, rubro o dirección.
    search_fields = ['cliente__nombres', 'cliente__apellidos', 'prestador__nombres',
                     'prestador__apellidos', 'rubro__nombre', 'direccion']

    def get_queryset(self):
        solicitudes = (Solicitud.objects.select_related('cliente', 'prestador', 'rubro')
                       .prefetch_related('seguimiento'))
        estado = self.request.query_params.get('estado')
        if estado:
            solicitudes = solicitudes.filter(estado=estado)
        return solicitudes

    # LAB 14 - EJ 11: TODO O NADA -> la solicitud y su primer seguimiento se guardan juntos.
    def perform_create(self, serializer):
        with transaction.atomic():
            prestador = serializer.validated_data['prestador']
            # El MONTO sale de la tarifa guardada en la base de datos, no del navegador.
            solicitud = serializer.save(monto=prestador.tarifa, estado='PEN')
            SeguimientoSolicitud.objects.create(solicitud=solicitud, estado='PEN',
                                                nota='Solicitud creada por el cliente')

    # LAB 14 - EJ 11: los ESTADOS AVANZAN EN ORDEN (Pendiente -> Confirmada -> ... -> Pagada).
    @action(detail=True, methods=['post'])
    def avanzar(self, request, pk=None):
        with transaction.atomic():
            solicitud = Solicitud.objects.select_for_update().get(pk=pk)
            siguiente = Solicitud.SIGUIENTE.get(solicitud.estado)
            if siguiente is None:
                return Response({'estado': f'Una solicitud {solicitud.get_estado_display()} ya no avanza.'},
                                status=400)
            solicitud.estado = siguiente
            solicitud.save()
            SeguimientoSolicitud.objects.create(solicitud=solicitud, estado=siguiente,
                                                nota=request.data.get('nota', ''))
        return Response(self.get_serializer(solicitud).data)
