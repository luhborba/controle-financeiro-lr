FROM python:3.12-slim

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Adicionar Poetry ao PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Diretório de trabalho
WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Instalar dependências (incluindo dev para desenvolvimento)
RUN poetry install --no-root

# Copiar código
COPY . .

# Criar usuário não-root
RUN useradd -m -u 1000 django && \
    chown -R django:django /app

USER django

# Expor porta
EXPOSE 8000

# Comando padrão
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

