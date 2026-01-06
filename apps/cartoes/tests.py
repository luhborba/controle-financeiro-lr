from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.cartoes.models import Cartao

User = get_user_model()


class CartaoModelTestCase(TestCase):
    """Testes para o modelo Cartao."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.cartao = Cartao.objects.create(
            usuario=self.usuario,
            nome='Nubank',
            bandeira='mastercard',
            limite=5000.00,
            dia_vencimento=10,
            dia_fechamento=5
        )
    
    def test_criacao_cartao(self):
        """Testa se o cartão foi criado corretamente."""
        self.assertEqual(self.cartao.nome, 'Nubank')
        self.assertEqual(self.cartao.bandeira, 'mastercard')
        self.assertEqual(self.cartao.limite, 5000.00)
        self.assertTrue(self.cartao.ativo)
    
    def test_str_cartao(self):
        """Testa a representação em string do cartão."""
        self.assertEqual(str(self.cartao), 'Nubank - Mastercard')
    
    def test_relacionamento_usuario(self):
        """Testa o relacionamento com usuário."""
        self.assertEqual(self.cartao.usuario, self.usuario)
        self.assertIn(self.cartao, self.usuario.cartoes.all())
    
    def test_dia_vencimento_valido(self):
        """Testa se dia de vencimento está no range correto."""
        self.assertGreaterEqual(self.cartao.dia_vencimento, 1)
        self.assertLessEqual(self.cartao.dia_vencimento, 31)
    
    def test_tabela_database(self):
        """Testa se o nome da tabela está correto."""
        self.assertEqual(Cartao._meta.db_table, 'Cartao')
