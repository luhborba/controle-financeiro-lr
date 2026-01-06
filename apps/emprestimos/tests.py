from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from decimal import Decimal
from apps.emprestimos.models import Emprestimo

User = get_user_model()


class EmprestimoModelTestCase(TestCase):
    """Testes para o modelo Emprestimo."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.emprestimo = Emprestimo.objects.create(
            usuario=self.usuario,
            credor='Banco XYZ',
            valor_total=10000.00,
            numero_parcelas=12,
            parcelas_pagas=3,
            taxa_juros=2.5,
            data_contratacao=date(2024, 1, 15)
        )
    
    def test_criacao_emprestimo(self):
        """Testa se o empréstimo foi criado corretamente."""
        self.assertEqual(self.emprestimo.credor, 'Banco XYZ')
        self.assertEqual(self.emprestimo.valor_total, Decimal('10000.00'))
        self.assertEqual(self.emprestimo.numero_parcelas, 12)
        self.assertEqual(self.emprestimo.parcelas_pagas, 3)
    
    def test_str_emprestimo(self):
        """Testa a representação em string do empréstimo."""
        self.assertEqual(str(self.emprestimo), 'Banco XYZ - 3/12')
    
    def test_valor_parcela(self):
        """Testa o cálculo do valor da parcela."""
        valor_esperado = Decimal('10000.00') / 12
        self.assertAlmostEqual(float(self.emprestimo.valor_parcela), float(valor_esperado), places=2)
    
    def test_saldo_restante(self):
        """Testa o cálculo do saldo restante."""
        parcelas_restantes = 12 - 3  # 9 parcelas
        valor_parcela = Decimal('10000.00') / 12
        saldo_esperado = valor_parcela * parcelas_restantes
        
        self.assertAlmostEqual(float(self.emprestimo.saldo_restante), float(saldo_esperado), places=2)
    
    def test_relacionamento_usuario(self):
        """Testa o relacionamento com usuário."""
        self.assertEqual(self.emprestimo.usuario, self.usuario)
        self.assertIn(self.emprestimo, self.usuario.emprestimos.all())
    
    def test_tabela_database(self):
        """Testa se o nome da tabela está correto."""
        self.assertEqual(Emprestimo._meta.db_table, 'Emprestimo')
