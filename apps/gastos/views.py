from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Gasto, MeioPagamento
from apps.categorias.models import Categoria
from apps.cartoes.models import Cartao
from apps.emprestimos.models import Emprestimo


@login_required
def lista_gastos(request):
    """Lista todos os gastos do usuário."""
    gastos = Gasto.objects.filter(
        usuario=request.user
    ).select_related('categoria', 'meio_pagamento', 'cartao').order_by('-data_gasto')
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    pago = request.GET.get('pago')
    
    if categoria_id:
        gastos = gastos.filter(categoria_id=categoria_id)
    
    if pago is not None:
        gastos = gastos.filter(pago=pago == 'true')
    
    context = {
        'gastos': gastos,
        'categorias': Categoria.objects.filter(ativo=True),
    }
    
    return render(request, 'gastos/lista.html', context)


@login_required
def criar_gasto(request):
    """Cria um novo gasto."""
    if request.method == 'POST':
        try:
            gasto = Gasto.objects.create(
                usuario=request.user,
                categoria_id=request.POST.get('categoria'),
                nome=request.POST.get('nome'),
                local=request.POST.get('local', ''),
                descricao=request.POST.get('descricao', ''),
                valor_total=request.POST.get('valor_total'),
                parcelado=request.POST.get('parcelado') == 'on',
                numero_parcelas=request.POST.get('numero_parcelas', 1),
                parcela_atual=request.POST.get('parcela_atual', 1),
                meio_pagamento_id=request.POST.get('meio_pagamento'),
                data_gasto=request.POST.get('data_gasto'),
                mes_referencia=request.POST.get('mes_referencia'),
                pago=request.POST.get('pago') == 'on',
            )
            
            # Cartão (opcional)
            if request.POST.get('cartao'):
                gasto.cartao_id = request.POST.get('cartao')
                gasto.save()
            
            messages.success(request, 'Gasto criado com sucesso!')
            
            # Se for HTMX, retorna apenas a linha da tabela
            if request.headers.get('HX-Request'):
                return render(request, 'gastos/partials/gasto_row.html', {'gasto': gasto})
            
            return redirect('gastos:lista')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar gasto: {str(e)}')
    
    context = {
        'categorias': Categoria.objects.filter(ativo=True),
        'meios_pagamento': MeioPagamento.objects.filter(usuario=request.user, ativo=True),
        'cartoes': Cartao.objects.filter(usuario=request.user, ativo=True),
    }
    
    return render(request, 'gastos/criar.html', context)


@login_required
def editar_gasto(request, pk):
    """Edita um gasto existente."""
    gasto = get_object_or_404(Gasto, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        try:
            gasto.categoria_id = request.POST.get('categoria')
            gasto.nome = request.POST.get('nome')
            gasto.local = request.POST.get('local', '')
            gasto.descricao = request.POST.get('descricao', '')
            gasto.valor_total = request.POST.get('valor_total')
            gasto.parcelado = request.POST.get('parcelado') == 'on'
            gasto.numero_parcelas = request.POST.get('numero_parcelas', 1)
            gasto.parcela_atual = request.POST.get('parcela_atual', 1)
            gasto.meio_pagamento_id = request.POST.get('meio_pagamento')
            gasto.data_gasto = request.POST.get('data_gasto')
            gasto.mes_referencia = request.POST.get('mes_referencia')
            gasto.pago = request.POST.get('pago') == 'on'
            
            if request.POST.get('cartao'):
                gasto.cartao_id = request.POST.get('cartao')
            
            gasto.save()
            
            messages.success(request, 'Gasto atualizado com sucesso!')
            return redirect('gastos:lista')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar gasto: {str(e)}')
    
    context = {
        'gasto': gasto,
        'categorias': Categoria.objects.filter(ativo=True),
        'meios_pagamento': MeioPagamento.objects.filter(usuario=request.user, ativo=True),
        'cartoes': Cartao.objects.filter(usuario=request.user, ativo=True),
    }
    
    return render(request, 'gastos/editar.html', context)


@login_required
@require_http_methods(["POST"])
def deletar_gasto(request, pk):
    """Deleta um gasto - Simplificado para funcionar com HTMX."""
    gasto = get_object_or_404(Gasto, pk=pk, usuario=request.user)
    gasto.delete()
    
    # HTMX: retorna vazio para remover a linha
    if request.headers.get('HX-Request'):
        return HttpResponse(status=200)
    
    messages.success(request, 'Gasto deletado com sucesso!')
    return redirect('gastos:lista')


@login_required
@require_http_methods(["POST"])
def marcar_pago(request, pk):
    """Marca/desmarca um gasto como pago (HTMX)."""
    gasto = get_object_or_404(Gasto, pk=pk, usuario=request.user)
    gasto.pago = not gasto.pago
    gasto.save()
    
    return render(request, 'gastos/partials/gasto_row.html', {'gasto': gasto})
