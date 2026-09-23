from django.contrib import admin
from apps.events.models import Evento, Inscricao, Certificado


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    """Configuração do admin para o model Evento."""

    list_display = (
        "titulo",
        "tipo",
        "data_inicio",
        "organizador",
        "vagas_totais",
        "is_active",
    )
    list_filter = ("tipo", "is_active")
    search_fields = ("titulo", "descricao")
    ordering = ("-data_inicio",)
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    """Configuração do admin para o model Inscricao."""

    list_display = (
        "evento",
        "participante",
        "presenca_confirmada",
        "data_checkin",
        "is_active",
    )
    list_filter = ("presenca_confirmada", "is_active")
    search_fields = ("evento__titulo", "participante__email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    """Configuração do admin para o model Certificado."""

    list_display = ("codigo_validacao", "inscricao", "data_emissao", "is_active")
    search_fields = (
        "codigo_validacao",
        "inscricao__evento__titulo",
        "inscricao__participante__email",
    )
    ordering = ("-data_emissao",)
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")