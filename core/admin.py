# Register your models here.
from django.contrib import admin
from .models import Veiculo, RegistroUso


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'marca', 'placa', 'ano', 'disponivel')
    search_fields = ('modelo', 'placa', 'marca')
    list_filter = ('disponivel', 'marca')


@admin.register(RegistroUso)
class RegistroUsoAdmin(admin.ModelAdmin):
    list_display = ('motorista', 'veiculo', 'status',
                    'km_inicial', 'km_final', 'data_solicitacao')
    list_filter = ('status', 'data_solicitacao')
    search_fields = ('motorista__username',
                     'veiculo__placa', 'veiculo__modelo')
