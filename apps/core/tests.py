from django.test import TestCase
from django.conf import settings


class ConfiguracaoTesteCase(TestCase):
    """Testes básicos de configuração do projeto."""
    
    def test_apps_instalados(self):
        """Verifica se todos os apps estão instalados."""
        apps_esperados = [
            'apps.core',
            'apps.categorias',
            'apps.cartoes',
            'apps.emprestimos',
            'apps.gastos',
            'apps.proventos',
            'apps.relatorios',
        ]
        
        for app in apps_esperados:
            self.assertIn(app, settings.INSTALLED_APPS)
    
    def test_banco_de_dados_configurado(self):
        """Verifica se o banco de dados PostgreSQL está configurado."""
        db_config = settings.DATABASES['default']
        self.assertEqual(db_config['ENGINE'], 'django.db.backends.postgresql')
    
    def test_timezone_configurado(self):
        """Verifica se timezone está configurado para São Paulo."""
        self.assertEqual(settings.TIME_ZONE, 'America/Sao_Paulo')
    
    def test_idioma_configurado(self):
        """Verifica se idioma está configurado para português."""
        self.assertEqual(settings.LANGUAGE_CODE, 'pt-br')

