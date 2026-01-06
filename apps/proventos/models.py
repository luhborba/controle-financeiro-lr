from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Provento(models.Model):
    """Modelo para proventos (receitas)."""
    
    class Meta:
        db_table = 'Provento'
        verbose_name = 'Provento'
        verbose_name_plural = 'Proventos'
        ordering = ['-data_recebimento']
    
    TIPO_PESSOA = [
        ('cpf', 'CPF'),
        ('cnpj', 'CNPJ'),
    ]
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='proventos'
    )
    descricao = models.CharField('Descrição', max_length=200)
    tipo_pessoa = models.CharField('Tipo Pessoa', max_length=4, choices=TIPO_PESSOA)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    data_recebimento = models.DateField('Data Recebimento')
    mes_referencia = models.DateField('Mês Referência')
    recebido = models.BooleanField('Recebido', default=False)
    observacoes = models.TextField('Observações', blank=True)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    
    def __str__(self):
        return f"{self.descricao} - R$ {self.valor:.2f}"
