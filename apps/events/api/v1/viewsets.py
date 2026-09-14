import uuid
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.commons.api.v1.viewsets import BaseModelApiViewSet, BaseReadOnlyModelViewSet
from apps.events.models import Certificado, Evento, Inscricao
from apps.events.api.v1.serializers import (
    CertificadoSerializer,
    EventoSerializer,
    InscricaoSerializer,
)

class EventoViewSet(BaseModelApiViewSet):
    """API ViewSet para Eventos.

    Fornece CRUD completo utilizando as regras de auditoria, soft delete
    e filtros automatizados do BaseModelApiViewSet.
    """

    model = Evento
    serializer_class = EventoSerializer

    def perform_create(self, serializer):
        """Sobrescreve para atribuir o usuário logado como organizador do evento."""
        if self.request.user.is_authenticated:
            serializer.validated_data["organizador"] = self.request.user
        super().perform_create(serializer)

class InscricaoViewSet(BaseModelApiViewSet):
    """API ViewSet para Inscrições em Eventos.

    Permite que participantes se inscrevam, listem suas inscrições
    e realizem a confirmação de presença (check-in).
    """

    model = Inscricao
    serializer_class = InscricaoSerializer

    def get_queryset(self):
        """Restringe a listagem padrão para usuários não-staff apenas às suas próprias inscrições."""
        queryset = super().get_queryset()
        if self.request and self.request.user.is_authenticated and not self.request.user.is_staff:
            return queryset.filter(participante=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """Garante que a inscrição fique vinculada ao participante logado."""
        if self.request.user.is_authenticated:
            serializer.validated_data["participante"] = self.request.user
        super().perform_create(serializer)

    @action(detail=False, methods=["get"], url_path="minhas-inscricoes")
    def minhas_inscricoes(self, request, *args, **kwargs):
        """Endpoint explícito para retornar todas as inscrições ativas do usuário logado."""
        queryset = self.model.objects.filter(participante=request.user, is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="check-in")
    def check_in(self, request, id=None, *args, **kwargs):
        """Realiza o check-in do participante no evento e gera o certificado caso elegível."""
        inscricao = self.get_object()

        if inscricao.presenca_confirmada:
            return Response(
                {"detail": "Check-in já realizado anteriormente."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        inscricao.presenca_confirmada = True
        inscricao.data_checkin = timezone.now()
        inscricao.updated_by = request.user
        inscricao.save()

        # Registra a alteração na auditoria
        self._log_on_update(self.get_serializer(inscricao))

        # Emissão automática de certificado se ainda não existir
        if not hasattr(inscricao, "certificado"):
            codigo_unico = str(uuid.uuid4()).replace("-", "").upper()[:16]
            Certificado.objects.create(
                inscricao=inscricao,
                codigo_validacao=codigo_unico,
                created_by=request.user,
            )

        return Response(
            {"detail": "Check-in realizado com sucesso e certificado emitido!"},
            status=status.HTTP_200_OK,
        )

class CertificadoViewSet(BaseReadOnlyModelViewSet):
    """API ViewSet para Certificados (Apenas Leitura).

    Permite consulta aos certificados gerados e validação pública.
    """

    model = Certificado
    serializer_class = CertificadoSerializer

    def get_queryset(self):
        """Filtra certificados visíveis apenas para o próprio participante (se não for staff)."""
        queryset = super().get_queryset()
        if self.request and self.request.user.is_authenticated and not self.request.user.is_staff:
            return queryset.filter(inscricao__participante=self.request.user)
        return queryset

    @action(
        detail=False,
        methods=["get"],
        url_path="validar",
        permission_classes=[AllowAny],
    )
    def validar(self, request, *args, **kwargs):
        """Endpoint público para conferência e validação de autenticidade do certificado.
        """
        codigo = request.query_params.get("codigo")
        if not codigo:
            return Response(
                {"detail": "O parâmetro 'codigo' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            certificado = self.model.objects.get(codigo_validacao=codigo, is_active=True)
            serializer = self.get_serializer(certificado)
            return Response(
                {"valido": True, "certificado": serializer.data},
                status=status.HTTP_200_OK,
            )
        except self.model.DoesNotExist:
            return Response(
                {"valido": False, "detail": "Certificado não encontrado ou inválido."},
                status=status.HTTP_404_NOT_FOUND,
            )

