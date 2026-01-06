from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from decimal import Decimal
from apps.gastos.models import MeioPagamento, Gasto
from apps.categorias.models import Categoria
from apps.cartoes.models import Cartao

User = get_user_model()


class MeioPagamentoModelTestCase(TestCase):
    """Testes para o modelo MeioPagamento."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.meio_pagamento = MeioPagamento.objects.create(
            usuario=self.usuario,
            nome='Cartão Crédito Principal',
            tipo='credito'
        )
    
    def test_criacao_meio_pagamento(self):
        """Testa se o meio de pagamento foi criado corretamente."""
        self.assertEqual(self.meio_pagamento.nome, 'Cartão Crédito Principal')
        self.assertEqual(self.meio_pagamento.tipo, 'credito')
        self.assertTrue(self.meio_pagamento.ativo)
    
    def test_str_meio_pagamento(self):
        """Testa a representação em string do meio de pagamento."""
        self.assertEqual(str(self.meio_pagamento), 'Cartão Crédito Principal (Crédito)')
    
    def test_tabela_database(self):
        """Testa se o nome da tabela está correto."""
        self.assertEqual(MeioPagamento._meta.db_table, 'MeioPagamento')


class GastoModelTestCase(TestCase):
    """Testes para o modelo Gasto."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.categoria = Categoria.objects.create(nome='Alimentação')
        
        self.meio_pagamento = MeioPagamento.objects.create(
            usuario=self.usuario,
            nome='PIX',
            tipo='pix'
        )
        
        self.cartao = Cartao.objects.create(
            usuario=self.usuario,
            nome='Nubank',
            bandeira='mastercard',
            limite=5000.00,
            dia_vencimento=10,
            dia_fechamento=5
        )
        
        self.gasto = Gasto.objects.create(
            usuario=self.usuario,
            categoria=self.categoria,
            nome='Supermercado',
            local='Carrefour',
            descricao='Compras do mês',
            valor_total=500.00,
            meio_pagamento=self.meio_pagamento,
            data_gasto=date(2024, 1, 15),
            mes_referencia=date(2024, 1, 1)
        )
    
    def test_criacao_gasto(self):
        """Testa se o gasto foi criado corretamente."""
        self.assertEqual(self.gasto.nome, 'Supermercado')
        self.assertEqual(self.gasto.valor_total, Decimal('500.00'))
        self.assertFalse(self.gasto.pago)
    
    def test_str_gasto_sem_parcelamento(self):
        """Testa a representação em string do gasto sem parcelamento."""
        self.assertEqual(str(self.gasto), 'Supermercado')
    
    def test_str_gasto_parcelado(self):
        """Testa a representação em string do gasto parcelado."""
        self.gasto.parcelado = True
        self.gasto.numero_parcelas = 3
        self.gasto.parcela_atual = 1
        self.gasto.save()
        
        self.assertEqual(str(self.gasto), 'Supermercado - 1/3')
    
    def test_valor_parcela_sem_parcelamento(self):
        """Testa o valor da parcela quando não é parcelado."""
        self.assertEqual(self.gasto.valor_parcela, Decimal('500.00'))
    
    def test_valor_parcela_parcelado(self):
        """Testa o cálculo do valor da parcela."""
        self.gasto.parcelado = True
        self.gasto.numero_parcelas = 5
        self.gasto.save()
        
        valor_esperado = Decimal('500.00') / 5
        self.assertEqual(self.gasto.valor_parcela, valor_esperado)
    
    def test_gasto_com_cartao(self):
        """Testa gasto vinculado a cartão."""
        self.gasto.cartao = self.cartao
        self.gasto.save()
        
        self.assertEqual(self.gasto.cartao, self.cartao)
        self.assertIn(self.gasto, self.cartao.gastos.all())
    
    def test_relacionamentos(self):
        """Testa os relacionamentos do gasto."""
        self.assertEqual(self.gasto.usuario, self.usuario)
        self.assertEqual(self.gasto.categoria, self.categoria)
        self.assertEqual(self.gasto.meio_pagamento, self.meio_pagamento)
    
    def test_tabela_database(self):
        """Testa se o nome da tabela está correto."""
        self.assertEqual(Gasto._meta.db_table, 'Gasto')
