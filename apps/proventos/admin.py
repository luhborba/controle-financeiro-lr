from django.contrib import admin
from .models import Provento


@admin.register(Provento)
class ProventoAdmin(admin.ModelAdmin):
    """Configuração do admin para Provento."""
    
    list_display = ['descricao', 'tipo_pessoa', 'valor', 'data_recebimento', 'recebido', 'usuario']
    list_filter = ['tipo_pessoa', 'recebido', 'data_recebimento', 'mes_referencia']
    search_fields = ['descricao', 'observacoes', 'usuario__email']
    readonly_fields = ['criado_em', 'atualizado_em']
    date_hierarchy = 'data_recebimento'
    
    fieldsets = (
        ('Informações do Provento', {
            'fields': ('usuario', 'descricao', 'tipo_pessoa', 'valor')
        }),
        ('Datas', {
            'fields': ('data_recebimento', 'mes_referencia')
        }),
        ('Status', {
            'fields': ('recebido', 'observacoes')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Filtra proventos para mostrar apenas do usuário logado (se não for superuser)."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)
