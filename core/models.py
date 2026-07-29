from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Veiculo(models.Model):
    placa = models.CharField(max_length=7, unique=True)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=30)
    ano = models.IntegerField()

    def __str__(self):
        return f"{self.modelo} ({self.placa})"


class RegistroUso(models.Model):
    # Opções para o status da solicitação
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente de Aprovação'),
        ('APROVADO', 'Aprovado / Em Uso'),
        ('RECUSADO', 'Recusado pelo Administrador'),
        ('CONCLUIDO', 'Concluído/Devolvido'),
    ]

    # Vincula a solicitação a um veículo e a um motorista (usuário) específico.
    veiculo = models.ForeignKey(
        Veiculo, on_delete=models.CASCADE, verbose_name="Veículo")
    motorista = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Motorista")

    # Dados de controle de tempo e status
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='PENDENTE')

    # Dados de quilometragem e observações
    km_inicial = models.IntegerField(verbose_name="KM inicial")
    km_final = models.IntegerField(
        verbose_name="KM Final", null=True, blank=True)
    observacoes = models.TextField(
        verbose_name="Observações", null=True, blank=True)

    def __str__(self):
        return f"{self.motorista.username} - {self.veiculo.modelo} ({self.status})"
