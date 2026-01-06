from django.contrib import admin
from .models import Emprestimo


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    """Configuração do admin para Emprestimo."""
    
    list_display = ['credor', 'valor_total', 'parcelas_info', 'taxa_juros', 'saldo_restante', 'ativo', 'usuario']
    list_filter = ['ativo', 'data_contratacao']
    search_fields = ['credor', 'usuario__email']
    readonly_fields = ['criado_em', 'atualizado_em', 'valor_parcela', 'saldo_restante']
    
    fieldsets = (
        ('Informações do Empréstimo', {
            'fields': ('usuario', 'credor', 'valor_total', 'taxa_juros', 'data_contratacao')
        }),
        ('Parcelamento', {
            'fields': ('numero_parcelas', 'parcelas_pagas')
        }),
        ('Cálculos', {
            'fields': ('valor_parcela', 'saldo_restante'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def parcelas_info(self, obj):
        """Exibe informação de parcelas."""
        return f"{obj.parcelas_pagas}/{obj.numero_parcelas}"
    parcelas_info.short_description = 'Parcelas'
    
    def get_queryset(self, request):
        """Filtra empréstimos para mostrar apenas do usuário logado (se não for superuser)."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)
