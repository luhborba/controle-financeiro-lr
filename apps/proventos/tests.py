from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from decimal import Decimal
from apps.proventos.models import Provento

User = get_user_model()


class ProventoModelTestCase(TestCase):
    """Testes para o modelo Provento."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.provento = Provento.objects.create(
            usuario=self.usuario,
            descricao='Salário Janeiro',
            tipo_pessoa='cnpj',
            valor=5000.00,
            data_recebimento=date(2024, 1, 5),
            mes_referencia=date(2024, 1, 1)
        )
    
    def test_criacao_provento(self):
        """Testa se o provento foi criado corretamente."""
        self.assertEqual(self.provento.descricao, 'Salário Janeiro')
        self.assertEqual(self.provento.tipo_pessoa, 'cnpj')
        self.assertEqual(self.provento.valor, Decimal('5000.00'))
        self.assertFalse(self.provento.recebido)
    
    def test_str_provento(self):
        """Testa a representação em string do provento."""
        self.assertEqual(str(self.provento), 'Salário Janeiro - R$ 5000.00')
    
    def test_provento_recebido(self):
        """Testa marcação de provento como recebido."""
        self.provento.recebido = True
        self.provento.save()
        
        provento_atualizado = Provento.objects.get(id=self.provento.id)
        self.assertTrue(provento_atualizado.recebido)
    
    def test_tipo_pessoa_cpf(self):
        """Testa criação de provento com CPF."""
        provento_cpf = Provento.objects.create(
            usuario=self.usuario,
            descricao='Freelance',
            tipo_pessoa='cpf',
            valor=1500.00,
            data_recebimento=date(2024, 1, 10),
            mes_referencia=date(2024, 1, 1)
        )
        
        self.assertEqual(provento_cpf.tipo_pessoa, 'cpf')
    
    def test_relacionamento_usuario(self):
        """Testa o relacionamento com usuário."""
        self.assertEqual(self.provento.usuario, self.usuario)
        self.assertIn(self.provento, self.usuario.proventos.all())
    
    def test_tabela_database(self):
        """Testa se o nome da tabela está correto."""
        self.assertEqual(Provento._meta.db_table, 'Provento')
