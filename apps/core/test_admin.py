from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class AdminTestCase(TestCase):
    """Testes para o Django Admin."""
    
    def setUp(self):
        """Configuração inicial dos testes."""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.client.login(username='admin', password='admin123')
    
    def test_admin_login(self):
        """Testa se consegue fazer login no admin."""
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_titulo_customizado(self):
        """Testa se o título do admin está customizado."""
        response = self.client.get(reverse('admin:index'))
        self.assertContains(response, 'Controle Financeiro LR')
    
    def test_categoria_admin_acessivel(self):
        """Testa se a listagem de categorias está acessível."""
        response = self.client.get(reverse('admin:categorias_categoria_changelist'))
        self.assertEqual(response.status_code, 200)
    
    def test_cartao_admin_acessivel(self):
        """Testa se a listagem de cartões está acessível."""
        response = self.client.get(reverse('admin:cartoes_cartao_changelist'))
        self.assertEqual(response.status_code, 200)
    
    def test_emprestimo_admin_acessivel(self):
        """Testa se a listagem de empréstimos está acessível."""
        response = self.client.get(reverse('admin:emprestimos_emprestimo_changelist'))
        self.assertEqual(response.status_code, 200)
    
    def test_gasto_admin_acessivel(self):
        """Testa se a listagem de gastos está acessível."""
        response = self.client.get(reverse('admin:gastos_gasto_changelist'))
        self.assertEqual(response.status_code, 200)
    
    def test_provento_admin_acessivel(self):
        """Testa se a listagem de proventos está acessível."""
        response = self.client.get(reverse('admin:proventos_provento_changelist'))
        self.assertEqual(response.status_code, 200)
