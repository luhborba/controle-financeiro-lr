from django.contrib import admin
from .models import Cartao


@admin.register(Cartao)
class CartaoAdmin(admin.ModelAdmin):
    """Configuração do admin para Cartao."""
    
    list_display = ['nome', 'bandeira', 'limite', 'dia_vencimento', 'dia_fechamento', 'ativo', 'usuario']
    list_filter = ['bandeira', 'ativo', 'criado_em']
    search_fields = ['nome', 'usuario__email']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações do Cartão', {
            'fields': ('usuario', 'nome', 'bandeira', 'limite')
        }),
        ('Datas de Cobrança', {
            'fields': ('dia_vencimento', 'dia_fechamento')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Filtra cartões para mostrar apenas do usuário logado (se não for superuser)."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)
