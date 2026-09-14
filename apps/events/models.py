import uuid
from django.db import models
from django.conf import settings
from apps.commons.models import BaseModel

class Evento(BaseModel):
    TIPO_CHOICES = (
        ('PRESENCIAL', 'Presencial'),
        ('ONLINE', 'Online'),
        ('HIBRIDO', 'Híbrido'),
    )

    organizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='eventos_criados'
    )
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='PRESENCIAL')
    local_presencial = models.TextField(
        blank=True, 
        null=True, 
        help_text="Endereço ou local caso seja presencial ou híbrido"
    )
    vagas_totais = models.PositiveIntegerField()
    carga_horaria_horas = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        db_table = 'eventos'
        ordering = ['-data_inicio']

    def __str__(self):
        return self.titulo

class Inscricao(BaseModel):
    evento = models.ForeignKey(
        Evento, 
        on_delete=models.CASCADE, 
        related_name='inscricoes'
    )
    participante = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='minhas_inscricoes'
    )
    presenca_confirmada = models.BooleanField(default=False)
    data_checkin = models.DateTimeField(blank=True, null=True)

    class Meta(BaseModel.Meta):
        db_table = 'inscricoes'
        constraints = [
            models.UniqueConstraint(
                fields=['evento', 'participante'], 
                condition=models.Q(is_active=True),
                name='unique_active_inscricao_evento_participante'
            )
        ]

    def __str__(self):
        return f"{self.participante} - {self.evento.titulo}"

class Certificado(BaseModel):
    inscricao = models.OneToOneField(
        Inscricao, 
        on_delete=models.CASCADE, 
        related_name='certificado'
    )
    codigo_validacao = models.CharField(max_length=64, unique=True)
    data_emissao = models.DateTimeField(auto_now_add=True)
    url_pdf = models.CharField(max_length=500, blank=True, null=True)

    class Meta(BaseModel.Meta):
        db_table = 'certificados'

    def __str__(self):
        return f"Certificado: {self.codigo_validacao}"
