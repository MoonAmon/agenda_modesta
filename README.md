# Documentação Técnica - Sistema de Gestão de Agendas e Orçamentos

**Cliente:** Claudio Modesto  
**Versão:** 1.0  
**Status:** Planejamento e Arquitetura

---

## 1. Resumo Executivo

Sistema web de gestão integrado, permitindo gerenciar agendas, clientes, projetos, orçamentos e recibos com integração nativa ao Google Calendar.

### Objetivos Principais

- Centralizar gestão de agendas com sincronização automática ao Google Calendar
- Automatizar geração de orçamentos e recibos em PDF
- Gerenciar clientes, projetos e histórico de atividades
- Calcular custos horários e valores automaticamente
- Enviar notificações de agendamentos via email (SMTP)

---

## 2. Funcionalidades Principais

### 2.1 Gestão de Agenda

- Integração bidirecional com Google Calendar
- Visualização de calendário com interface intuitiva
- Agendamento público para clientes
- Notificações automáticas por email (SMTP)
- Sistema de confirmação de agendamentos
- Histórico completo de agendas

### 2.2 Gestão de Clientes e Projetos

- CRUD completo de clientes
- Associação de múltiplos projetos por cliente
- Histórico de interações e transações
- Rastreamento de status de projetos
- Detalhes de contato e informações complementares

### 2.3 Configuração de Custo Horário

- Define valor hora padrão
- Suporte a múltiplas taxas por tipo de serviço
- Cálculo automático de custos em orçamentos e recibos
- Histórico de alterações de taxas

### 2.4 Gerador de Orçamentos

- Cálculo automático de valores baseado em horas estimadas
- Numeração automática e sequencial
- Geração em PDF com branding do cliente
- Histórico de orçamentos por cliente/projeto

### 2.5 Gerador de Recibos

- Numeração automática e sequencial
- Cálculo automático de valores
- Geração em PDF profissional
- Rastreamento de recibos emitidos

---

## 3. Stack Tecnológico

### Backend

| Tecnologia            | Versão | Propósito              |
| --------------------- | ------ | ---------------------- |
| Python                | 3.11+  | Linguagem base         |
| Django                | 5.0+   | Framework web          |
| Django REST Framework | 3.14+  | API REST               |
| PostgreSQL            | 14+    | Banco de dados         |
| Celery                | 5.3+   | Tarefas assíncronas    |
| Redis                 | 7.0+   | Cache e message broker |

### Integrações Externas

| Serviço             | Propósito                | Autenticação |
| ------------------- | ------------------------ | ------------ |
| Google Calendar API | Sincronização de agendas | OAuth 2.0    |
| SMTP                | Envio de notificações    | Credenciais  |
| Reportlab           | Geração de PDFs          | -            |

### Frontend

| Tecnologia           | Propósito                       |
| -------------------- | ------------------------------- |
| HTML5                | Markup semântico                |
| CSS3 / Tailwind      | Estilização responsiva          |
| HTMX 1.9+            | Requisições AJAX sem JavaScript |
| Django Templates     | Renderização de partials        |
| Alpine.js (opcional) | Interatividade client-side      |

### Ferramentas de Desenvolvimento

| Ferramenta | Propósito            |
| ---------- | -------------------- |
| Git/GitHub | Controle de versão   |
| Docker     | Containerização      |
| pytest     | Testes unitários     |
| Coverage   | Análise de cobertura |

---

## 4. Arquitetura do Projeto

### 4.1 Estrutura de Diretórios

projeto_freelance/
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── .gitignore
│
├── config/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
│
├── apps/
│ ├── users/
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ ├── urls.py
│ │ └── tests.py
│ │
│ ├── clientes/
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ ├── urls.py
│ │ └── tests.py
│ │
│ ├── projetos/
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ ├── urls.py
│ │ └── tests.py
│ │
│ ├── agenda/
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ ├── urls.py
│ │ ├── google_calendar.py
│ │ ├── tasks.py
│ │ └── tests.py
│ │
│ ├── orcamentos/
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ ├── urls.py
│ │ ├── pdf_generator.py
│ │ └── tests.py
│ │
│ ├── recibos/
│ │ ├── models.py
│ │ ├── views.py
│ │ ├── serializers.py
│ │ ├── urls.py
│ │ ├── pdf_generator.py
│ │ └── tests.py
│ │
│ └── custos/
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ └── urls.py
│
├── templates/
│ ├── base.html
│ ├── dashboard.html
│ ├── agenda/
│ ├── clientes/
│ ├── projetos/
│ ├── orcamentos/
│ └── recibos/
│
├── static/
│ ├── css/
│ ├── js/
│ └── images/
│
├── media/
│ └── pdfs/
│
└── tests/
├── conftest.py
└── factories.py

### 4.2 Modelos de Dados

#### User (Autenticação)

- id (UUID)
- email (EmailField, unique)
- nome_completo (CharField)
- senha (PasswordField, hashed)
- custo_horario_padrao (DecimalField)
- logo_empresa (ImageField, opcional)
- data_criacao (DateTimeField)
- ativo (BooleanField)

#### Cliente

- id (UUID)
- usuario (ForeignKey → User)
- nome (CharField)
- email (EmailField)
- telefone (CharField)
- cpf_cnpj (CharField)
- endereco (TextField, opcional)
- cidade (CharField)
- data_criacao (DateTimeField)
- data_atualizacao (DateTimeField)
- ativo (BooleanField)
- historico (Relacionamento reverso)

#### Projeto

- id (UUID)
- cliente (ForeignKey → Cliente)
- usuario (ForeignKey → User)
- nome (CharField)
- descricao (TextField)
- status (ChoiceField: planejamento, em_andamento, concluido, cancelado)
- data_inicio (DateField)
- data_prevista_conclusao (DateField)
- data_conclusao (DateField, opcional)
- data_criacao (DateTimeField)
- historico (Relacionamento reverso)

#### Custo Horário

- id (UUID)
- usuario (ForeignKey → User)
- descricao (CharField)
- valor_hora (DecimalField)
- ativo (BooleanField)
- data_criacao (DateTimeField)
- data_atualizacao (DateTimeField)

#### Agenda (Event)

- id (UUID)
- usuario (ForeignKey → User)
- cliente (ForeignKey → Cliente, opcional)
- projeto (ForeignKey → Projeto, opcional)
- titulo (CharField)
- descricao (TextField)
- data_inicio (DateTimeField)
- data_fim (DateTimeField)
- local (CharField, opcional)
- google_calendar_id (CharField, unique, opcional)
- confirmado (BooleanField)
- notificacao_enviada (BooleanField)
- data_criacao (DateTimeField)
- data_atualizacao (DateTimeField)

#### Orçamento

- id (UUID)
- usuario (ForeignKey → User)
- cliente (ForeignKey → Cliente)
- projeto (ForeignKey → Projeto, opcional)
- numero_sequencial (IntegerField)
- data_emissao (DateField)
- data_validade (DateField)
- descricao (TextField)
- horas_estimadas (DecimalField)
- valor_hora (DecimalField)
- valor_total (DecimalField, auto-calculado)
- status (ChoiceField: rascunho, enviado, aceito, rejeitado)
- pdf_gerado (FileField)
- data_criacao (DateTimeField)
- data_atualizacao (DateTimeField)

#### Recibo

- id (UUID)
- usuario (ForeignKey → User)
- cliente (ForeignKey → Cliente)
- projeto (ForeignKey → Projeto, opcional)
- numero_sequencial (IntegerField)
- data_emissao (DateField)
- descricao (TextField)
- horas_trabalhadas (DecimalField)
- valor_hora (DecimalField)
- valor_total (DecimalField, auto-calculado)
- forma_pagamento (ChoiceField: dinheiro, pix, transferencia, cartao)
- status_pagamento (ChoiceField: pendente, pago)
- pdf_gerado (FileField)
- data_criacao (DateTimeField)
- data_atualizacao (DateTimeField)

---

## 5. Integração com Google Calendar

### 5.1 Fluxo de Autenticação

1. Usuário clica em "Conectar Google Calendar"
2. Redirecionamento para Google OAuth 2.0 (pode mudar)
3. Autorização de escopos específicos
4. Armazenamento seguro do access token e refresh token
5. Sincronização inicial de eventos

### 5.2 Sincronização Bidirecional

**Sincronização de Saída (Django → Google):**

- Novo evento criado no Django
- Enviado para Google Calendar via API
- ID do Google armazenado para referência
- Atualizações posteriores sincronizadas

**Sincronização de Entrada (Google → Django):**

- Tarefa Celery em background executada a cada 5 minutos
- Busca eventos modificados no Google Calendar
- Atualiza registros correspondentes no Django
- Detecta exclusões e sincroniza

### 5.3 Escopos de Permissão Solicitados

SCOPES = [
'https://www.googleapis.com/auth/calendar',
'https://www.googleapis.com/auth/calendar.events'
]

---

## 6. Sistema de Notificações via SMTP

### 6.1 Eventos de Notificação

| Evento              | Destinatário | Conteúdo                       |
| ------------------- | ------------ | ------------------------------ |
| Agendamento Criado  | Cliente      | Confirmação com data/hora      |
| Agendamento Próximo | Cliente      | Lembrança 24h antes            |
| Orçamento Enviado   | Cliente      | Link para visualizar orçamento |
| Recibo Gerado       | Cliente      | Recibo em anexo                |

### 6.2 Configuração SMTP

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

---

## 7. Geração de PDFs

### 7.1 Tecnologia: ReportLab

Biblioteca escolhida para geração de PDFs dinâmicos com suporte a:

- Templates customizáveis
- Imagens (logo, assinatura)
- Cálculos automáticos

## 8. HTMX Integration

### 8.1 Por que HTMX?

**Benefícios:**

- ✓ Interatividade sem JavaScript complexo
- ✓ Server-driven UI mantém lógica centralizada no Django
- ✓ Reduz código frontend significativamente
- ✓ Compatibilidade com Django templates nativa
- ✓ Melhor performance que SPA para aplicações de negócio
- ✓ Progressive enhancement - funciona sem JS

---

## 9. Cronograma de Desenvolvimento

### Fase 1: Planejamento e Design

- [x] Definição de requisitos detalhados
- [x] Arquitetura do sistema
- [ ] Design de wireframes e mockups
- [ ] Configuração inicial do projeto Django

### Fase 2: Desenvolvimento Backend

- [ ] Setup do banco de dados PostgreSQL
- [ ] Modelos Django (User, Cliente, Projeto, etc.)
- [ ] API REST com Django REST Framework
- [ ] Integração Google Calendar API
- [ ] Sistema de autenticação e autorização
- [ ] Gerador de PDFs (Orçamentos e Recibos)
- [ ] Sistema de notificações SMTP

### Fase 3: Desenvolvimento Frontend com HTMX

- [ ] Dashboard principal com atualizações dinâmicas
- [ ] Módulo de Agenda com calendário interativo (HTMX)
- [ ] Gerenciamento de Clientes com busca real-time
- [ ] Gerenciamento de Projetos com filtros dinâmicos
- [ ] Gerador de Orçamentos com preview HTMX
- [ ] Gerador de Recibos com template do cliente
- [ ] Responsividade para mobile com HTMX
- [ ] Loading indicators e feedback visual

### Fase 4: Testes e QA

- [ ] Testes unitários (pytest)
- [ ] Testes de integração
- [ ] Testes end-to-end
- [ ] Testes de performance
- [ ] Testes de segurança

### Fase 5: Deploy e Documentação

- [ ] Configuração de ambiente de produção
- [ ] Setup do servidor (Docker)
- [ ] Documentação API
- [ ] Documentação de usuário
- [ ] Deploy em produção

---

## 9. Dependências do Projeto

### requirements.txt

Django==5.0.1
djangorestframework==3.14.0
django-cors-headers==4.3.1
django-environ==0.21.0
django-htmx==1.17.0
psycopg2-binary==2.9.9
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
google-api-python-client==2.108.0
celery==5.3.4
redis==5.0.1
reportlab==4.0.9
Pillow==10.1.0
python-decouple==3.8
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0
gunicorn==21.2.0
whitenoise==6.6.0

---

## 10. Variáveis de Ambiente (.env)

# Django

DEBUG=False
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1,seu-dominio.com

# Database

DB_ENGINE=django.db.backends.postgresql
DB_NAME=projeto_freelance
DB_USER=postgres
DB_PASSWORD=sua-senha-postgres
DB_HOST=localhost
DB_PORT=5432

# Google Calendar

GOOGLE_CLIENT_ID=seu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=seu-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/callback

# SMTP

EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app
DEFAULT_FROM_EMAIL=noreply@seudominio.com

# Redis

REDIS_URL=redis://localhost:6379/0

# Celery

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Segurança

CSRF_TRUSTED_ORIGINS=http://localhost:8000,https://seu-dominio.com

---

## 11. Instruções de Setup Inicial

### 11.1 Requisitos do Sistema

- Python 3.11+
- PostgreSQL 14+
- Redis 7.0+
- Git
- Docker

### 11.2 Instalação Local

# Clonar repositório

git clone https://github.com/usuario/projeto_freelance.git
cd projeto_freelance

# Criar ambiente virtual

python -m venv venv
source venv/bin/activate # ou: venv\Scripts\activate (Windows)

# Instalar dependências

pip install -r requirements.txt

# Copiar arquivo de exemplo

cp .env.example .env

# Editar variáveis de ambiente

nano .env

# Executar migrações

python manage.py migrate

# Criar superusuário

python manage.py createsuperuser

# Coletar arquivos estáticos

python manage.py collectstatic --noinput

# Executar servidor

python manage.py runserver

### 11.3 Usando Docker

# Build das imagens

docker-compose build

# Executar containers

docker-compose up -d

# Executar migrações

docker-compose exec web python manage.py migrate

# Criar superusuário

docker-compose exec web python manage.py createsuperuser

# Acessar aplicação

http://localhost:8000

---

## 12. Testes

### 12.1 Executar Testes

# Todos os testes

pytest

# Com coverage

pytest --cov=apps --cov-report=html

# Testes específicos

pytest apps/agenda/tests.py

### 12.2 Cobertura Esperada

- Backend: 80%+
- Modelos: 90%+
- Views: 75%+
- Serializers: 70%+

---

## 13. Padrões HTMX no Projeto

### 13.1 Detecção de Requisições HTMX

Verificar se requisição veio de HTMX (com middleware django-htmx):

def meu_view(request):
if request.htmx: # Retornar apenas o partial template
return render(request, 'partial.html', context)
else: # Retornar página completa
return render(request, 'full_page.html', context)

### 13.2 Convenção de Partials

- Templates normais: `templates/app/modelo_list.html`
- Partials HTMX: `templates/app/_modelo_list.html` (com underscore)

templates/
├── clientes/
│ ├── list.html # Página completa
│ ├── detail.html # Página completa
│ ├── \_list.html # Partial para HTMX
│ ├── \_form.html # Partial de formulário
│ └── \_item.html # Partial de item único

### 13.3 Retorno de Erros com Status Correto

def update_orcamento(request, pk):
form = OrcamentoForm(request.POST, instance=orcamento)

    if form.is_valid():
        form.save()
        return render(request, 'orcamentos/_item.html', {'orcamento': orcamento})

    # HTMX vai interpretar 400 como erro e não fazer swap padrão
    return render(request, 'orcamentos/_form.html',
                 {'form': form}, status=400)

### 13.4 Polling para Atualizações

<!-- Atualizar agenda a cada 30 segundos -->
<div hx-get="{% url 'agenda:updates' %}"
     hx-trigger="every 30s"
     hx-swap="innerHTML">
    Carregando eventos...
</div>

### 13.5 Swapping Strategies

<!-- innerHTML: substitui conteúdo interno (padrão) -->
<div hx-get="..." hx-swap="innerHTML">...</div>

<!-- outerHTML: substitui elemento inteiro -->
<div hx-get="..." hx-swap="outerHTML">...</div>

<!-- beforeend: adiciona ao final (para infinite scroll) -->
<div hx-get="..." hx-swap="beforeend">...</div>

<!-- afterbegin: adiciona no início -->
<div hx-get="..." hx-swap="afterbegin">...</div>

<!-- beforebegin: insere antes do elemento -->
<div hx-get="..." hx-swap="beforebegin">...</div>

<!-- delete: remove elemento após sucesso -->
<div hx-delete="..." hx-swap="swap:1s then delete">...</div>

<!-- Swap com transição -->
<div hx-get="..." hx-swap="innerHTML swap:0.5s">...</div>

---

## 14. Segurança

### 13.1 Boas Práticas Implementadas

- ✓ HTTPS obrigatório em produção
- ✓ CSRF protection ativado
- ✓ SQL injection prevention (ORM Django)
- ✓ Autenticação via OAuth 2.0
- ✓ Tokens de acesso com expiração
- ✓ Rate limiting na API
- ✓ Variáveis sensíveis em .env
- ✓ Senhas hasheadas (PBKDF2)
- ✓ Validação de entrada em formulários

### 13.2 Checklist de Segurança para Deploy

- [ ] `DEBUG = False` em produção
- [ ] `SECRET_KEY` alterada e segura
- [ ] `ALLOWED_HOSTS` configurado
- [ ] HTTPS com certificado SSL válido
- [ ] Database backups automáticos
- [ ] Logs centralizados
- [ ] Rate limiting ativado
- [ ] Firewall configurado
- [ ] Senhas SMTP seguras

---

## 15. Endpoints da API REST

### Autenticação

POST /api/auth/register/ - Registrar novo usuário
POST /api/auth/login/ - Login
POST /api/auth/logout/ - Logout
POST /api/auth/refresh-token/ - Renovar token

### Clientes

GET /api/clientes/ - Listar clientes
POST /api/clientes/ - Criar cliente
GET /api/clientes/{id}/ - Detalhar cliente
PUT /api/clientes/{id}/ - Atualizar cliente
DELETE /api/clientes/{id}/ - Deletar cliente

### Projetos

GET /api/projetos/ - Listar projetos
POST /api/projetos/ - Criar projeto
GET /api/projetos/{id}/ - Detalhar projeto
PUT /api/projetos/{id}/ - Atualizar projeto
DELETE /api/projetos/{id}/ - Deletar projeto

### Agenda

GET /api/agenda/ - Listar eventos
POST /api/agenda/ - Criar evento
GET /api/agenda/{id}/ - Detalhar evento
PUT /api/agenda/{id}/ - Atualizar evento
DELETE /api/agenda/{id}/ - Deletar evento
POST /api/agenda/sincronizar/ - Sincronizar com Google

### Orçamentos

GET /api/orcamentos/ - Listar orçamentos
POST /api/orcamentos/ - Criar orçamento
GET /api/orcamentos/{id}/ - Detalhar orçamento
PUT /api/orcamentos/{id}/ - Atualizar orçamento
GET /api/orcamentos/{id}/pdf/ - Download PDF

### Recibos

GET /api/recibos/ - Listar recibos
POST /api/recibos/ - Criar recibo
GET /api/recibos/{id}/ - Detalhar recibo
PUT /api/recibos/{id}/ - Atualizar recibo
GET /api/recibos/{id}/pdf/ - Download PDF

### Custos

GET /api/custos/ - Listar custos horários
POST /api/custos/ - Criar custo
PUT /api/custos/{id}/ - Atualizar custo

---

## 16. Referências e Recursos

### HTMX

- [HTMX Official Documentation](https://htmx.org/)
- [django-htmx Package](https://django-htmx.readthedocs.io/)
- [HTMX + Django Patterns](https://github.com/adamchainz/django-htmx-patterns)
- [HTMX with Django REST Framework](https://testdriven.io/blog/drf-vue-vs-django-htmx/)

### Documentação Técnica

### Documentação Oficial

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Google Calendar API](https://developers.google.com/calendar/api/guides/overview)
- [ReportLab](https://www.reportlab.com/)
- [Celery](https://docs.celeryproject.org/)
- [PostgreSQL](https://www.postgresql.org/docs/)

### Ferramentas de Suporte

- Postman (teste de API)
- pgAdmin (gerenciamento PostgreSQL)
- Redis Commander (monitoramento Redis)
- Docker Desktop (containerização)

---

**Versão:** 1.0  
**Autor:** Thiago Amancio
**Status:** Planejamento e Design
