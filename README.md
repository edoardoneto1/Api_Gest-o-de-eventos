# Boilerplate JWT

API moderna baseada em Django REST Framework, autenticação JWT, arquivos estáticos e de mídia, múltiplos ambientes (local e produção), documentação interativa, e infraestrutura totalmente conteinerizada com Docker.

---

## 🧱 Estrutura do Projeto

```bash
boilerplate-jwt/
├── apps/                        # Aplicações Django
├── boilerplatejwt/                # Core do projeto
│   ├── settings/                # Configurações por ambiente
│   ├── router/                  # Rotas principais
│   ├── static/ & staticfiles/   # Arquivos estáticos
│   ├── media/ & mediafiles/     # Arquivos de mídia
│   ├── logs/                    # Logs da aplicação
│   ├── celery.py                # Configuração do Celery
│   ├── asgi.py / wsgi.py        # Entry points ASGI/WSGI
│   ├── storage_backends.py      # Armazenamento customizado
│   └── urls.py                  # Rotas principais
├── docker/                      # Dockerfiles e configurações
├── .envs/                       # Variáveis de ambiente
├── tools/                       # Scripts utilitários
├── scripts/                     # Scripts de auxílio para o deploy automatizado
├── manage.py                    # Comando de gerenciamento
├── Makefile                     # Comandos úteis com `make`
├── postman_collection.json      # Coleção para testes
└── README.md                    # Este arquivo
```

---

## 🚀 Requisitos

- [Docker Engine](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

---

## ▶️ Comandos Úteis

### Inicializar o projeto

```bash
make build
make up
```

### Rebuild de imagem + reload

```bash
make build-api reload-api
```

### Acessar o Admin do Django

- URL: [http://localhost:8000](http://localhost:8000)
- Login: `admin@boilerplatejwt.com.br`
- Senha: `UNIFIP@123`

---

## 🔐 Autenticação

A autenticação é feita via JWT, com endpoints padrão do Simple JWT. O token pode ser usado nos headers com `Authorization: Bearer <token>`.

---

## 📚 Documentação da API

- Swagger: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)
- CoreAPI: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

---

## 💌 Coleção Postman

Importe o arquivo [`postman_collection.json`](postman_collection.json) no Postman para testar os endpoints rapidamente.

---

## 🛠 Funcionalidades

- Django 5+ com DRF
- Suporte a múltiplos ambientes (`local.py`, `production.py`)
- Configuração de storage customizado
- Gerador automático de logs
- Deploy automatizado via `deploy.sh`, com criação de imagens de backup

---

## 🧪 Testes

Rodar testes locais (caso configurado):

```bash
make test
```
