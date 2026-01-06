from django.contrib import admin
from .models import MeioPagamento, Gasto


@admin.register(MeioPagamento)
class MeioPagamentoAdmin(admin.ModelAdmin):
    """Configuração do admin para MeioPagamento."""
    
    list_display = ['nome', 'tipo', 'ativo', 'usuario']
    list_filter = ['tipo', 'ativo']
    search_fields = ['nome', 'usuario__email']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações do Meio de Pagamento', {
            'fields': ('usuario', 'nome', 'tipo', 'ativo')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Filtra meios de pagamento para mostrar apenas do usuário logado (se não for superuser)."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)


@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    """Configuração do admin para Gasto."""
    
    list_display = ['nome', 'categoria', 'valor_total', 'parcelamento_info', 'data_gasto', 'pago', 'usuario']
    list_filter = ['categoria', 'pago', 'parcelado', 'data_gasto', 'mes_referencia']
    search_fields = ['nome', 'local', 'descricao', 'usuario__email']
    readonly_fields = ['criado_em', 'atualizado_em', 'valor_parcela']
    date_hierarchy = 'data_gasto'
    
    fieldsets = (
        ('Informações do Gasto', {
            'fields': ('usuario', 'categoria', 'nome', 'local', 'descricao', 'valor_total')
        }),
        ('Parcelamento', {
            'fields': ('parcelado', 'numero_parcelas', 'parcela_atual', 'valor_parcela')
        }),
        ('Vinculação', {
            'fields': ('cartao', 'emprestimo', 'meio_pagamento')
        }),
        ('Controle', {
            'fields': ('data_gasto', 'mes_referencia', 'pago')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def parcelamento_info(self, obj):
        """Exibe informação de parcelamento."""
        if obj.parcelado:
            return f"{obj.parcela_atual}/{obj.numero_parcelas} (R$ {obj.valor_parcela:.2f})"
        return "À vista"
    parcelamento_info.short_description = 'Parcelamento'
    
    def get_queryset(self, request):
        """Filtra gastos para mostrar apenas do usuário logado (se não for superuser)."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)
