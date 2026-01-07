from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from decimal import Decimal
from django.urls import reverse
from .models import Gasto, MeioPagamento
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


class GastoViewsTestCase(TestCase):
    """Testes para as views de Gasto."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.categoria = Categoria.objects.create(nome='Alimentação')
        
        self.meio_pagamento = MeioPagamento.objects.create(
            usuario=self.usuario,
            nome='PIX',
            tipo='pix'
        )
        
        self.gasto = Gasto.objects.create(
            usuario=self.usuario,
            categoria=self.categoria,
            nome='Supermercado',
            valor_total=100.00,
            meio_pagamento=self.meio_pagamento,
            data_gasto=date(2024, 1, 15),
            mes_referencia=date(2024, 1, 1)
        )
    
    def test_lista_gastos_autenticado(self):
        """Testa se usuário autenticado consegue ver a lista."""
        response = self.client.get(reverse('gastos:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Supermercado')
    
    def test_lista_gastos_nao_autenticado(self):
        """Testa se usuário não autenticado é redirecionado."""
        self.client.logout()
        response = self.client.get(reverse('gastos:lista'))
        self.assertEqual(response.status_code, 302)  # Redirect para login
    
    def test_criar_gasto(self):
        """Testa criação de gasto."""
        data = {
            'categoria': self.categoria.id,
            'nome': 'Padaria',
            'valor_total': '50.00',
            'meio_pagamento': self.meio_pagamento.id,
            'data_gasto': '2024-01-16',
            'mes_referencia': '2024-01-01',
        }
        response = self.client.post(reverse('gastos:criar'), data)
        
        # Deve redirecionar para lista após criar
        self.assertEqual(response.status_code, 302)
        
        # Verifica se foi criado
        self.assertTrue(Gasto.objects.filter(nome='Padaria').exists())
        novo_gasto = Gasto.objects.get(nome='Padaria')
        self.assertEqual(novo_gasto.valor_total, Decimal('50.00'))
    
    def test_editar_gasto(self):
        """Testa edição de gasto."""
        data = {
            'categoria': self.categoria.id,
            'nome': 'Supermercado Atacadão',  # Nome alterado
            'valor_total': '150.00',  # Valor alterado
            'meio_pagamento': self.meio_pagamento.id,
            'data_gasto': '2024-01-15',
            'mes_referencia': '2024-01-01',
        }
        response = self.client.post(
            reverse('gastos:editar', kwargs={'pk': self.gasto.id}), 
            data
        )
        
        # Deve redirecionar para lista
        self.assertEqual(response.status_code, 302)
        
        # Recarrega do banco
        self.gasto.refresh_from_db()
        
        # Verifica se foi alterado
        self.assertEqual(self.gasto.nome, 'Supermercado Atacadão')
        self.assertEqual(self.gasto.valor_total, Decimal('150.00'))
    
    def test_editar_gasto_com_parcelamento(self):
        """Testa edição de gasto incluindo parcelamento."""
        data = {
            'categoria': self.categoria.id,
            'nome': 'Compra Parcelada',
            'valor_total': '300.00',
            'meio_pagamento': self.meio_pagamento.id,
            'data_gasto': '2024-01-15',
            'mes_referencia': '2024-01-01',
            'parcelado': 'on',
            'numero_parcelas': '3',
            'parcela_atual': '1',
        }
        response = self.client.post(
            reverse('gastos:editar', kwargs={'pk': self.gasto.id}), 
            data
        )
        
        self.assertEqual(response.status_code, 302)
        
        self.gasto.refresh_from_db()
        
        self.assertTrue(self.gasto.parcelado)
        self.assertEqual(self.gasto.numero_parcelas, 3)
        self.assertEqual(self.gasto.parcela_atual, 1)
        self.assertEqual(self.gasto.valor_total, Decimal('300.00'))
    
    def test_deletar_gasto(self):
        """Testa exclusão de gasto."""
        gasto_id = self.gasto.id
        
        response = self.client.post(
            reverse('gastos:deletar', kwargs={'pk': gasto_id})
        )
        
        # Deve redirecionar para lista
        self.assertEqual(response.status_code, 302)
        
        # Verifica se foi deletado
        self.assertFalse(Gasto.objects.filter(id=gasto_id).exists())
    
    def test_deletar_gasto_htmx(self):
        """Testa exclusão de gasto via HTMX."""
        gasto_id = self.gasto.id
        
        response = self.client.post(
            reverse('gastos:deletar_htmx', kwargs={'pk': gasto_id}),
            HTTP_HX_REQUEST='true'
        )
        
        # Deve retornar 200 (vazio)
        self.assertEqual(response.status_code, 200)
        
        # Verifica se foi deletado
        self.assertFalse(Gasto.objects.filter(id=gasto_id).exists())
    
    def test_deletar_gasto_htmx_sem_header(self):
        """Testa que delete HTMX não funciona sem header HX-Request."""
        response = self.client.post(
            reverse('gastos:deletar_htmx', kwargs={'pk': self.gasto.id})
        )
        
        # Deve retornar 405 (método não permitido)
        self.assertEqual(response.status_code, 405)
        
        # Gasto não deve ser deletado
        self.assertTrue(Gasto.objects.filter(id=self.gasto.id).exists())
    
    def test_marcar_pago_htmx(self):
        """Testa marcação de gasto como pago via HTMX."""
        self.assertFalse(self.gasto.pago)
        
        response = self.client.post(
            reverse('gastos:marcar_pago', kwargs={'pk': self.gasto.id}),
            HTTP_HX_REQUEST='true'
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Recarrega do banco
        self.gasto.refresh_from_db()
        
        # Verifica se foi marcado como pago
        self.assertTrue(self.gasto.pago)
    
    def test_marcar_pago_toggle(self):
        """Testa que marcar como pago funciona como toggle."""
        # Marca como pago
        self.client.post(
            reverse('gastos:marcar_pago', kwargs={'pk': self.gasto.id}),
            HTTP_HX_REQUEST='true'
        )
        self.gasto.refresh_from_db()
        self.assertTrue(self.gasto.pago)
        
        # Desmarca
        self.client.post(
            reverse('gastos:marcar_pago', kwargs={'pk': self.gasto.id}),
            HTTP_HX_REQUEST='true'
        )
        self.gasto.refresh_from_db()
        self.assertFalse(self.gasto.pago)
    
    def test_usuario_nao_pode_editar_gasto_de_outro(self):
        """Testa se usuário não consegue editar gasto de outro usuário."""
        outro_usuario = User.objects.create_user(
            username='outro',
            email='outro@example.com',
            password='senha123'
        )
        
        gasto_outro = Gasto.objects.create(
            usuario=outro_usuario,
            categoria=self.categoria,
            nome='Gasto do Outro',
            valor_total=200.00,
            meio_pagamento=self.meio_pagamento,
            data_gasto=date(2024, 1, 15),
            mes_referencia=date(2024, 1, 1)
        )
        
        # Tenta editar gasto de outro usuário
        response = self.client.get(
            reverse('gastos:editar', kwargs={'pk': gasto_outro.id})
        )
        
        # Deve retornar 404 (não encontrado)
        self.assertEqual(response.status_code, 404)
    
    def test_usuario_nao_pode_deletar_gasto_de_outro(self):
        """Testa se usuário não consegue deletar gasto de outro usuário."""
        outro_usuario = User.objects.create_user(
            username='outro',
            email='outro@example.com',
            password='senha123'
        )
        
        gasto_outro = Gasto.objects.create(
            usuario=outro_usuario,
            categoria=self.categoria,
            nome='Gasto do Outro',
            valor_total=200.00,
            meio_pagamento=self.meio_pagamento,
            data_gasto=date(2024, 1, 15),
            mes_referencia=date(2024, 1, 1)
        )
        
        # Tenta deletar gasto de outro usuário
        response = self.client.post(
            reverse('gastos:deletar', kwargs={'pk': gasto_outro.id})
        )
        
        # Deve retornar 404
        self.assertEqual(response.status_code, 404)
        
        # Gasto não deve ser deletado
        self.assertTrue(Gasto.objects.filter(id=gasto_outro.id).exists())
    
    def test_formulario_editar_carrega_dados_corretos(self):
        """Testa se formulário de edição carrega os dados corretos."""
        response = self.client.get(
            reverse('gastos:editar', kwargs={'pk': self.gasto.id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Supermercado')
        self.assertContains(response, '100')  # Valor
        self.assertContains(response, self.categoria.nome)
    
    def test_filtro_por_categoria(self):
        """Testa filtro de gastos por categoria."""
        # Criar outra categoria e gasto
        outra_categoria = Categoria.objects.create(nome='Transporte')
        Gasto.objects.create(
            usuario=self.usuario,
            categoria=outra_categoria,
            nome='Uber',
            valor_total=30.00,
            meio_pagamento=self.meio_pagamento,
            data_gasto=date(2024, 1, 16),
            mes_referencia=date(2024, 1, 1)
        )
        
        # Filtrar por categoria "Alimentação"
        response = self.client.get(
            reverse('gastos:lista'),
            {'categoria': self.categoria.id}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Supermercado')
        self.assertNotContains(response, 'Uber')
    
    def test_filtro_por_status_pago(self):
        """Testa filtro de gastos por status pago."""
        # Criar gasto pago
        Gasto.objects.create(
            usuario=self.usuario,
            categoria=self.categoria,
            nome='Gasto Pago',
            valor_total=50.00,
            meio_pagamento=self.meio_pagamento,
            data_gasto=date(2024, 1, 16),
            mes_referencia=date(2024, 1, 1),
            pago=True
        )
        
        # Filtrar apenas pagos
        response = self.client.get(
            reverse('gastos:lista'),
            {'pago': 'true'}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gasto Pago')
        self.assertNotContains(response, 'Supermercado')  # Não está pago
