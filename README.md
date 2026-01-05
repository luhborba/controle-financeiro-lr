# Controle Financeiro LR Data Consult

Sistema de controle financeiro pessoal multi-usuário.

![CI Status](https://github.com/SEU_USUARIO/controle-financeiro-lr/workflows/Testes%20Automatizados/badge.svg)

## 📋 Sobre

Aplicação web para gestão de:
- 💰 Gastos (parcelados ou à vista)
- 💳 Cartões de crédito
- 📊 Empréstimos
- 💵 Proventos (CPF/CNPJ)

## 🚀 Tecnologias

- Python 3.12
- Django 5.0
- PostgreSQL 16
- Docker + Docker Compose
- HTMX + Alpine.js + Tailwind CSS

## 🔀 Estratégia de Branches

### `dev` (desenvolvimento)
- Branch principal de trabalho
- Todos os commits vão aqui
- CI roda testes automaticamente

### `main` (produção)
- Código estável em produção
- **Protegida**: só aceita merge via Pull Request
- **Requisito**: testes devem passar (cobertura ≥ 70%)
- Deploy automático após merge

## �� Workflow de Desenvolvimento
```bash
# 1. Trabalhar na branch dev
git checkout dev
git pull origin dev

# 2. Desenvolver e commitar
git add .
git commit -m "feat: adiciona gestão de cartões"
git push origin dev

# 3. Quando estiver pronto para produção
# Criar Pull Request: dev → main no GitHub

# 4. Se testes passarem → merge aprovado → deploy automático
```

## 📝 Padrão de Commits (Conventional Commits)

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `test:` Adiciona/corrige testes
- `docs:` Documentação
- `refactor:` Refatoração
- `chore:` Manutenção

## 🧪 Testes
```bash
# Rodar testes localmente
docker-compose exec web pytest

# Com cobertura
docker-compose exec web pytest --cov=apps --cov-report=html

# Ver relatório
open htmlcov/index.html
```

**Requisito mínimo de cobertura: 70%**

## 📦 Instalação
```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/controle-financeiro-lr.git
cd controle-financeiro-lr

# 2. Checkout branch dev
git checkout dev

# 3. Configure variáveis
cp .env.example .env
# Edite o .env

# 4. Suba containers
docker-compose up -d

# 5. Execute migrations
docker-compose exec web python manage.py migrate

# 6. Crie superusuário
docker-compose exec web python manage.py createsuperuser

# 7. Acesse
http://localhost:8000
```

## 🔐 Deploy (Restrito)

Deploy automático via GitHub Actions.

**Requisitos para deploy:**
✅ Pull Request de `dev` → `main`  
✅ Todos os testes passando  
✅ Cobertura de código ≥ 70%  
✅ Aprovação manual do PR  

Apenas o autor original pode fazer merge para `main`.

## 📄 Licença

MIT License - Código aberto, deploy restrito.

