from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Emprestimo(models.Model):
    """Modelo para empréstimos."""
    
    class Meta:
        db_table = 'Emprestimo'
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
        ordering = ['-data_contratacao']
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='emprestimos'
    )
    credor = models.CharField('Credor', max_length=200)
    valor_total = models.DecimalField('Valor Total', max_digits=10, decimal_places=2)
    numero_parcelas = models.IntegerField('Número de Parcelas')
    parcelas_pagas = models.IntegerField('Parcelas Pagas', default=0)
    taxa_juros = models.DecimalField(
        'Taxa de Juros (%)',
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text='Taxa de juros mensal em percentual'
    )
    data_contratacao = models.DateField('Data Contratação')
    ativo = models.BooleanField('Ativo', default=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    def __str__(self):
        return f"{self.credor} - {self.parcelas_pagas}/{self.numero_parcelas}"
    
    @property
    def valor_parcela(self):
        """Calcula o valor aproximado de cada parcela (sem juros compostos)."""
        if self.numero_parcelas > 0:
            return self.valor_total / self.numero_parcelas
        return self.valor_total
    
    @property
    def saldo_restante(self):
        """Calcula o saldo restante a pagar."""
        parcelas_restantes = self.numero_parcelas - self.parcelas_pagas
        return self.valor_parcela * parcelas_restantes
