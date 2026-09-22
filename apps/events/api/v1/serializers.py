from django.utils import timezone
from rest_framework import serializers

from apps.commons.api.v1.serializers import UUIDPrimaryKeyRelatedField
from apps.events.models import Certificado, Evento, Inscricao


class EventoSerializer(serializers.ModelSerializer):
    organizador_nome = serializers.ReadOnlyField(source="organizador.get_full_name")
    vagas_restantes = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = [
            "id",
            "titulo",
            "descricao",
            "organizador",
            "organizador_nome",
            "data_inicio",
            "data_fim",
            "tipo",
            "local_presencial",
            "vagas_totais",
            "vagas_restantes",
            "carga_horaria_horas",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "organizador", "is_active", "created_at", "updated_at"]

    def get_vagas_restantes(self, obj):
        inscricoes_ativas = obj.inscricoes.filter(is_active=True).count()
        return max(0, obj.vagas_totais - inscricoes_ativas)

    def validate(self, attrs):
        data_inicio = attrs.get("data_inicio", getattr(self.instance, "data_inicio", None))
        data_fim = attrs.get("data_fim", getattr(self.instance, "data_fim", None))

        if data_inicio and data_fim and data_fim <= data_inicio:
            raise serializers.ValidationError({
                "data_fim": "A data final do evento deve ser posterior à data de início."
            })
        return attrs


class InscricaoSerializer(serializers.ModelSerializer):
    evento = UUIDPrimaryKeyRelatedField(
        queryset=Evento.objects.filter(is_active=True)
    )
    evento_detalhes = EventoSerializer(source="evento", read_only=True)
    participante_nome = serializers.ReadOnlyField(source="participante.get_full_name")
    evento_titulo = serializers.ReadOnlyField(source="evento.titulo")

    class Meta:
        model = Inscricao
        fields = [
            "id",
            "evento",
            "evento_detalhes",
            "evento_titulo",
            "participante",
            "participante_nome",
            "presenca_confirmada",
            "data_checkin",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "participante",
            "presenca_confirmada",
            "data_checkin",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        """Força o campo 'evento' a retornar o UUID (não o pkid)."""
        representation = super().to_representation(instance)
        representation["evento"] = str(instance.evento.id)
        return representation

    def validate_evento(self, value):
        if not value.is_active:
            raise serializers.ValidationError(
                "Não é possível se inscrever em um evento inativo."
            )

        if value.data_fim < timezone.now():
            raise serializers.ValidationError(
                "Não é possível se inscrever em um evento que já encerrou."
            )

        vagas_preenchidas = value.inscricoes.filter(is_active=True).count()
        if vagas_preenchidas >= value.vagas_totais:
            raise serializers.ValidationError(
                "Este evento não possui mais vagas disponíveis."
            )

        return value

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        evento = attrs.get("evento")

        if user and user.is_authenticated and evento:
            if Inscricao.objects.filter(
                evento=evento, participante=user, is_active=True
            ).exists():
                raise serializers.ValidationError(
                    "Você já está inscrito neste evento."
                )

        return attrs


class CertificadoSerializer(serializers.ModelSerializer):
    participante_nome = serializers.ReadOnlyField(source="inscricao.participante.get_full_name")
    evento_titulo = serializers.ReadOnlyField(source="inscricao.evento.titulo")
    carga_horaria = serializers.ReadOnlyField(source="inscricao.evento.carga_horaria_horas")

    class Meta:
        model = Certificado
        fields = [
            "id",
            "inscricao",
            "codigo_validacao",
            "participante_nome",
            "evento_titulo",
            "carga_horaria",
            "data_emissao",
            "url_pdf",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "codigo_validacao",
            "data_emissao",
            "url_pdf",
            "is_active",
            "created_at",
            "updated_at",
        ]
