# chamba/api_urls.py
# config/urls.py monta estas rutas bajo /api/chamba/.

from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register('prestadores', api_views.PrestadorViewSet, basename='prestador')

urlpatterns = router.urls
