from rest_framework.routers import DefaultRouter
from apps.events.api.v1.viewsets import (
    CertificadoViewSet,
    EventoViewSet,
    InscricaoViewSet,
)

app_name = "events"

router = DefaultRouter()
router.register(r"eventos", EventoViewSet, basename="evento")
router.register(r"inscricoes", InscricaoViewSet, basename="inscricao")
router.register(r"certificados", CertificadoViewSet, basename="certificado")

urlpatterns = router.urls