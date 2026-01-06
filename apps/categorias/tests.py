from django.test import TestCase
from apps.categorias.models import Categoria


class CategoriaModelTestCase(TestCase):
    """Testes para o modelo Categoria."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.categoria = Categoria.objects.create(
            nome='Alimentação',
            descricao='Gastos com alimentação'
        )
    
    def test_criacao_categoria(self):
        """Testa se a categoria foi criada corretamente."""
        self.assertEqual(self.categoria.nome, 'Alimentação')
        self.assertEqual(self.categoria.descricao, 'Gastos com alimentação')
        self.assertTrue(self.categoria.ativo)
    
    def test_str_categoria(self):
        """Testa a representação em string da categoria."""
        self.assertEqual(str(self.categoria), 'Alimentação')
    
    def test_nome_unico(self):
        """Testa se o nome da categoria é único."""
        from django.db import IntegrityError
        
        with self.assertRaises(IntegrityError):
            Categoria.objects.create(nome='Alimentação')
    
    def test_categoria_inativa(self):
        """Testa desativação de categoria."""
        self.categoria.ativo = False
        self.categoria.save()
        
        categoria_atualizada = Categoria.objects.get(id=self.categoria.id)
        self.assertFalse(categoria_atualizada.ativo)
    
    def test_tabela_database(self):
        """Testa se o nome da tabela está correto."""
        self.assertEqual(Categoria._meta.db_table, 'Categoria')
