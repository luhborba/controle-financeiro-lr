from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MeioPagamento(models.Model):
    """Modelo para meios de pagamento."""
    
    class Meta:
        db_table = 'MeioPagamento'
        verbose_name = 'Meio de Pagamento'
        verbose_name_plural = 'Meios de Pagamento'
        ordering = ['nome']
    
    TIPOS = [
        ('dinheiro', 'Dinheiro'),
        ('pix', 'PIX'),
        ('debito', 'Débito'),
        ('credito', 'Crédito'),
        ('transferencia', 'Transferência'),
        ('boleto', 'Boleto'),
    ]
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='meios_pagamento'
    )
    nome = models.CharField('Nome', max_length=100)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPOS)
    ativo = models.BooleanField('Ativo', default=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class Gasto(models.Model):
    """Modelo para registro de gastos."""
    
    class Meta:
        db_table = 'Gasto'
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ['-data_gasto']
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='gastos'
    )
    categoria = models.ForeignKey(
        'categorias.Categoria',
        on_delete=models.PROTECT,
        verbose_name='Categoria',
        related_name='gastos'
    )
    nome = models.CharField('Nome', max_length=200)
    local = models.CharField('Local', max_length=200, blank=True)
    descricao = models.TextField('Descrição', blank=True)
    valor_total = models.DecimalField('Valor Total', max_digits=10, decimal_places=2)
    
    # Parcelamento
    parcelado = models.BooleanField('Parcelado', default=False)
    numero_parcelas = models.IntegerField('Número de Parcelas', default=1)
    parcela_atual = models.IntegerField('Parcela Atual', default=1)
    
    # Vinculação
    cartao = models.ForeignKey(
        'cartoes.Cartao',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Cartão',
        related_name='gastos'
    )
    emprestimo = models.ForeignKey(
        'emprestimos.Emprestimo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Empréstimo',
        related_name='gastos'
    )
    meio_pagamento = models.ForeignKey(
        MeioPagamento,
        on_delete=models.PROTECT,
        verbose_name='Meio de Pagamento',
        related_name='gastos'
    )
    
    # Controle
    data_gasto = models.DateField('Data do Gasto')
    pago = models.BooleanField('Pago', default=False)
    mes_referencia = models.DateField('Mês Referência')
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    def __str__(self):
        if self.parcelado:
            return f"{self.nome} - {self.parcela_atual}/{self.numero_parcelas}"
        return self.nome
    
    @property
    def valor_parcela(self):
        """Calcula o valor de cada parcela."""
        if self.parcelado and self.numero_parcelas > 0:
            return self.valor_total / self.numero_parcelas
        return self.valor_total
