from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Cartao(models.Model):
    """Modelo para cartões de crédito."""
    
    class Meta:
        db_table = 'Cartao'
        verbose_name = 'Cartão'
        verbose_name_plural = 'Cartões'
        ordering = ['nome']
    
    BANDEIRAS = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('elo', 'Elo'),
        ('amex', 'American Express'),
        ('hipercard', 'Hipercard'),
        ('outro', 'Outro'),
    ]
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='cartoes'
    )
    nome = models.CharField('Nome', max_length=100)
    bandeira = models.CharField('Bandeira', max_length=50, choices=BANDEIRAS)
    limite = models.DecimalField('Limite', max_digits=10, decimal_places=2)
    dia_vencimento = models.IntegerField('Dia Vencimento', help_text='Dia do mês (1-31)')
    dia_fechamento = models.IntegerField('Dia Fechamento', help_text='Dia do mês (1-31)')
    ativo = models.BooleanField('Ativo', default=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    def __str__(self):
        return f"{self.nome} - {self.get_bandeira_display()}"
