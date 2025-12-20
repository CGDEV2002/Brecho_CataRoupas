# E-commerce de Brechó

**E-commerce de Brechó — Django + API REST**

Full Stack com Python e Django no backend, API REST com Django REST Framework. Django ORM com SQLite para desenvolvimento e PostgreSQL para produção, sistema de templates Django e Bootstrap 5 no frontend. Sistema CRUD completo para gerenciamento de produtos e categorias, carrinho de compras com sessões, upload de imagens com Pillow. API REST com autenticação, filtros avançados e interface browsable automática. Gunicorn como servidor WSGI e python-dotenv para segurança das variáveis de ambiente. Deploy otimizado com Whitenoise para arquivos estáticos, configurado para PythonAnywhere e Vercel com CI/CD automatizado via GitHub.

## Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **Django 5.1.4+** - Framework web
- **Django REST Framework** - API REST completa
- **Django ORM** - Mapeamento objeto-relacional
- **SQLite** - Banco de dados (desenvolvimento)
- **PostgreSQL** - Banco de dados (produção)
- **Gunicorn** - Servidor WSGI para produção
- **Whitenoise** - Servir arquivos estáticos
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **dj-database-url** - Configuração de banco via URL
- **psycopg2-binary** - Adapter PostgreSQL
- **django-filter** - Filtros avançados para API

### Frontend
- **Django Templates** - Sistema de templates
- **Bootstrap 5** - Framework CSS
- **Bootstrap Icons** - Ícones
- **HTML5/CSS3**
- **JavaScript**

### Upload e Mídia
- **Pillow** - Processamento de imagens
- **Django FileField/ImageField** - Upload de arquivos

### Deploy
- **Vercel** - Hospedagem e deploy
- **PythonAnywhere** - Opção de hospedagem gratuita
- **GitHub Actions** - CI/CD automatizado

## Funcionalidades

### Catálogo de Produtos
- Sistema completo de produtos com categorias
- Upload e gerenciamento de imagens
- Classificação por tamanho (PP, P, M, G, GG, XG, EXG)
- Estados de conservação (Novo, Semi-novo, Usado)
- Sistema de slugs para URLs amigáveis
- Controle de disponibilidade

### Carrinho de Compras
- Carrinho baseado em sessões (não requer login)
- Adicionar/remover produtos
- Controle de quantidade
- Cálculo automático de subtotais
- Persistência durante a navegação

### Interface Admin
- Painel administrativo Django customizado
- Gerenciamento de produtos e categorias
- Sistema de usuários e permissões
- Interface intuitiva para upload de imagens

### API REST Completa
- **Endpoints públicos**: Consulta de produtos e categorias
- **Endpoints protegidos**: Criação/edição apenas para admins
- **Interface Browsable**: Interface web automática para testes
- **Filtros avançados**: Busca, categoria, tamanho, condição, ordenação
- **Paginação automática**: Performance otimizada
- **Endpoints customizados**: Produtos em destaque e agrupamentos
- **Autenticação por sessão**: Integrada com Django Admin
- **JSON estruturado**: Dados organizados para consumo

### Sistema de Navegação
- Página inicial com produtos em destaque
- Páginas de detalhes dos produtos
- Navegação por categorias
- Design responsivo

## Instalação e Configuração

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/ecommerce.git
cd ecommerce
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Execute as migrações
```bash
python manage.py migrate
```

### 6. Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
```

### 7. Colete arquivos estáticos
```bash
python manage.py collectstatic
```

### 8. Execute o servidor de desenvolvimento
```bash
python manage.py runserver
```

O projeto estará disponível em `http://localhost:8000/`

## Estrutura do Projeto

```
ecommerce/
├── brecho/                 # Configurações principais do Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py        # Configurações do projeto
│   ├── urls.py           # URLs principais
│   └── wsgi.py
├── loja/                  # App principal da loja
│   ├── models.py         # Modelos (Produto, Categoria)
│   ├── views.py          # Views da loja
│   ├── urls.py           # URLs da loja
│   ├── admin.py          # Configuração do admin
│   └── migrations/       # Migrações do banco
├── carrinho/             # App do carrinho de compras
│   ├── models.py         # Modelo do CarrinhoItem
│   ├── views.py          # Views do carrinho
│   └── urls.py           # URLs do carrinho
├── templates/            # Templates Django
│   ├── base.html         # Template base
│   ├── loja/             # Templates da loja
│   └── carrinho/         # Templates do carrinho
├── static/               # Arquivos estáticos
│   └── img/              # Imagens do site
├── media/                # Uploads de usuários
│   └── produtos/         # Imagens dos produtos
├── manage.py             # Script de gerenciamento Django
├── requirements.txt      # Dependências Python
├── runtime.txt          # Versão do Python para deploy
├── vercel.json          # Configuração Vercel
└── .env                 # Variáveis de ambiente (não commitado)
```

## Modelos de Dados

### Produto
- **nome**: Nome do produto
- **slug**: URL amigável
- **descricao**: Descrição detalhada
- **preco**: Preço em decimal
- **categoria**: Relacionamento com Categoria
- **tamanho**: Choices (PP, P, M, G, GG, XG, EXG)
- **condicao**: Choices (novo, seminovo, usado)
- **disponivel**: Boolean
- **imagem**: ImageField para upload

### Categoria
- **nome**: Nome da categoria
- **slug**: URL amigável

### CarrinhoItem
- **session_key**: Chave da sessão
- **produto**: Relacionamento com Produto
- **quantidade**: Quantidade do produto
- **criado_em**: Timestamp

## API REST Endpoints

### Produtos
```
GET    /api/produtos/                    # Lista produtos (público)
POST   /api/produtos/                    # Criar produto (admin)
GET    /api/produtos/{slug}/             # Detalhe produto (público)
PUT    /api/produtos/{slug}/             # Atualizar produto (admin)
DELETE /api/produtos/{slug}/             # Deletar produto (admin)
GET    /api/produtos/destaques/          # Produtos em destaque (público)
GET    /api/produtos/por_categoria/      # Produtos agrupados (público)
```

### Categorias
```
GET    /api/categorias/                  # Lista categorias (público)
GET    /api/categorias/{slug}/           # Detalhe categoria (público)
```

### Filtros e Busca
```
GET    /api/produtos/?search=termo       # Busca por nome/descrição
GET    /api/produtos/?categoria=1        # Filtrar por categoria
GET    /api/produtos/?tamanho=M          # Filtrar por tamanho
GET    /api/produtos/?condicao=novo      # Filtrar por condição
GET    /api/produtos/?ordering=preco     # Ordenar por preço
GET    /api/produtos/?page=2             # Paginação
```

## Deploy

### Opção 1: PythonAnywhere (Gratuito)
1. Crie uma conta no PythonAnywhere
2. Upload do código via Git ou arquivo
3. Configure o ambiente virtual
4. Configure as variáveis de ambiente
5. Configure o WSGI e arquivos estáticos

### Opção 2: Vercel (Recomendado)
1. Conecte seu repositório GitHub ao Vercel
2. Configure as variáveis de ambiente
3. Deploy automático a cada push

### Opção 3: Railway
1. Conecte com GitHub
2. Configure PostgreSQL
3. Deploy automático

Para instruções detalhadas, consulte o [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md).

### API REST
Para implementar a API REST, consulte o [API_REST_GUIDE.md](API_REST_GUIDE.md).

## Variáveis de Ambiente

### Desenvolvimento
```env
DEBUG=True
SECRET_KEY=sua-chave-local
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Produção
```env
DEBUG=False
SECRET_KEY=chave-super-forte-50-caracteres
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
DATABASE_URL=postgres://usuario:senha@host:porta/database
```

## Scripts Utilitários

### Popular dados de exemplo
```bash
python populate_data.py
```

### Backup do banco
```bash
python manage.py dumpdata > backup.json
```

### Restaurar backup
```bash
python manage.py loaddata backup.json
```

### Testar API REST
```bash
# Iniciar servidor
python manage.py runserver

# Acessar interface da API
# http://127.0.0.1:8000/api/

# Testar endpoints
# http://127.0.0.1:8000/api/produtos/
# http://127.0.0.1:8000/api/categorias/
# http://127.0.0.1:8000/api/produtos/?search=short
```

## Troubleshooting

### Problema: Página padrão Django aparece
- Verifique se `DEBUG=False` em produção
- Confirme se as URLs estão configuradas corretamente
- Verifique `ALLOWED_HOSTS`

### Problema: Imagens não carregam
- Execute `python manage.py collectstatic`
- Verifique configurações de `STATIC_URL` e `MEDIA_URL`
- Confirme se Whitenoise está configurado

### Problema: Erro 500 em produção
- Verifique logs do servidor
- Confirme configurações de banco de dados
- Verifique se todas as dependências estão instaladas

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Para dúvidas ou sugestões, abra uma issue no GitHub ou entre em contato através do email.

## Status do Projeto

- [x] Sistema básico de produtos e categorias
- [x] Carrinho de compras com sessões
- [x] Upload de imagens
- [x] Interface administrativa
- [x] Deploy automatizado
- [x] **API REST completa com DRF**
- [x] **Filtros avançados e paginação**
- [x] **Interface Browsable para testes**
- [x] **Autenticação e permissões**
- [ ] Sistema de pagamento
- [ ] Sistema de usuários e autenticação
- [ ] Sistema de pedidos
- [ ] Notificações por email
- [ ] Sistema de avaliações
- [ ] Autenticação JWT para apps móveis

## Demonstração

### Links de Demonstração

#### Site Principal
- **Gratuito**: [cataroupasbrecho.pythonanywhere.com](https://cataroupasbrecho.pythonanywhere.com)
- **Domínio próprio**: [cataroupasbrecho.com](https://cataroupasbrecho.com) (quando configurado)

#### API REST
- **Interface API**: [cataroupasbrecho.pythonanywhere.com/api/](https://cataroupasbrecho.pythonanywhere.com/api/)
- **Produtos**: [cataroupasbrecho.pythonanywhere.com/api/produtos/](https://cataroupasbrecho.pythonanywhere.com/api/produtos/)
- **Categorias**: [cataroupasbrecho.pythonanywhere.com/api/categorias/](https://cataroupasbrecho.pythonanywhere.com/api/categorias/)
- **Busca**: [cataroupasbrecho.pythonanywhere.com/api/produtos/?search=short](https://cataroupasbrecho.pythonanywhere.com/api/produtos/?search=short)
- **Filtros**: [cataroupasbrecho.pythonanywhere.com/api/produtos/?tamanho=M](https://cataroupasbrecho.pythonanywhere.com/api/produtos/?tamanho=M)

### Credenciais Admin
Após executar `python manage.py createsuperuser`, acesse:
- **Django Admin**: `/admin/`
- **API com permissões**: `/api/produtos/` (após login no admin)
- Use as credenciais criadas durante o setup

### Teste de Segurança da API
1. **Sem login**: Pode apenas visualizar dados (GET)
2. **Com login admin**: Pode criar/editar/deletar (POST/PUT/DELETE)
3. **Interface automática**: Browsable API para testes visuais
