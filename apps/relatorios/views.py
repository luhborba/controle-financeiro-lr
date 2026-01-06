from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from apps.gastos.models import Gasto
from apps.proventos.models import Provento
from apps.cartoes.models import Cartao


@login_required
def dashboard(request):
    """View do dashboard principal."""
    
    # Mês atual
    hoje = date.today()
    mes_atual = date(hoje.year, hoje.month, 1)
    
    # Totais do mês
    total_gastos = Gasto.objects.filter(
        usuario=request.user,
        mes_referencia=mes_atual
    ).aggregate(total=Sum('valor_total'))['total'] or 0
    
    total_proventos = Provento.objects.filter(
        usuario=request.user,
        mes_referencia=mes_atual
    ).aggregate(total=Sum('valor'))['total'] or 0
    
    saldo = total_proventos - total_gastos
    
    # Últimos gastos
    ultimos_gastos = Gasto.objects.filter(
        usuario=request.user
    ).select_related('categoria').order_by('-data_gasto')[:5]
    
    # Cartões ativos
    total_cartoes = Cartao.objects.filter(usuario=request.user, ativo=True).count()
    
    # Próximos vencimentos
    proximos_vencimentos = Cartao.objects.filter(
        usuario=request.user,
        ativo=True
    ).order_by('dia_vencimento')[:5]
    
    context = {
        'total_gastos': total_gastos,
        'total_proventos': total_proventos,
        'saldo': saldo,
        'ultimos_gastos': ultimos_gastos,
        'total_cartoes': total_cartoes,
        'proximos_vencimentos': proximos_vencimentos,
    }
    
    return render(request, 'dashboard/index.html', context)
