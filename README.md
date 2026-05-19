# 🛒 Django E-commerce API

> Projeto desenvolvido para a disciplina de Desenvolvimento Web  
> **Pós-Graduação em Desenvolvimento de Sistemas - IFTO**

---

## 👨‍🏫 Professor
**Fabio Vidal**

## 👥 Equipe

| Nome | Papel |
|------|-------|
| Carlos Jorge Sarmento Neto | Desenvolvedor Full-Stack |

---

## 📋 Sobre o Projeto

API RESTful para sistema de **E-commerce** desenvolvida com Django e Django REST Framework.  
Projeto acadêmico com foco em boas práticas de desenvolvimento, arquitetura de APIs e segurança.

### 🎯 Objetivos do Projeto

- Compreender os conceitos de **API RESTful** e sua importância na arquitetura moderna de sistemas
- Implementar um sistema completo de e-commerce com **separação de responsabilidades**
- Utilizar o **Django ORM** para manipulação segura do banco de dados
- Aprender sobre **serialização** de dados e comunicação entre backend e frontend
- Aplicar conceitos de **segurança** contra SQL Injection e outras vulnerabilidades

---

## 🎨 Frontend e Interface

### Tecnologias de Interface

| Tecnologia | Versão | Finalidade |
|------------|--------|-------------|
| **Bootstrap 4** | 4.6.2 | Layout responsivo e componentes |
| **Bootstrap 5** | 5.3.0 | Componentes modernos e ícones |
| **Font Awesome** | 6.x | Ícones vetoriais |
| **jQuery** | 3.6.0 | Manipulação do DOM e AJAX |
| **Popper.js** | 2.11+ | Tooltips e popovers do Bootstrap |

### CDNs Utilizadas

```html
<!-- Bootstrap 4 -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>

<!-- Bootstrap 5 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Font Awesome -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

<!-- jQuery -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
```

### 📊 Funcionalidades Implementadas

#### ✅ Concluídas
- [x] Sistema de busca de produtos com parâmetros GET
- [x] API de configurações do site (Settings, Banners, Carrossel)
- [x] Listagem de produtos com filtros (categoria, preço, nome)
- [x] Sistema de avaliações de produtos (rating 1-5 estrelas)
- [x] Carrinho de compras persistente por usuário
- [x] Sistema de pedidos e cálculo de valores
- [x] Autenticação de usuários (login, registro, perfil)
- [x] Interface administrativa (Django Admin)

#### 🚧 Em desenvolvimento
- [ ] Sistema de pagamentos integrados
- [ ] Envio de e-mails de confirmação
- [ ] Relatórios de vendas
- [ ] Dashboard administrativo

---

## 🛠 Tecnologias Utilizadas

### Backend
| Tecnologia | Versão | Finalidade |
|------------|--------|-------------|
| **Python** | 3.14+ | Linguagem principal |
| **Django** | 6.0.4 | Framework web |
| **Django REST Framework** | 3.14+ | Criação da API REST |
| **SQLite** | 3.x | Banco de dados (desenvolvimento) |
| **Pillow** | 10.x | Manipulação de imagens |

### Ferramentas de Desenvolvimento
- **Git** - Controle de versão
- **Virtualenv** - Isolamento de dependências
- **VS Code** - IDE de desenvolvimento

---

## 🏗️ Arquitetura do Projeto

### Estrutura de Diretórios

``` 
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Interface)                  │
│            HTML, CSS, JavaScript, Bootstrap              │
└─────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────┐
│                   API REST (Camada de Interface)         │
│              Serializers, Views API, URLs API            │
│                    Formatos: JSON                        │
└─────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────┐
│                 Django ORM (Abstração de Dados)          │
│         Models, Querysets, Managers                      │
│         Proteção automática contra SQL Injection         │
└─────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────┐
│              Banco de Dados (Persistência)               │
│                     SQLite / PostgreSQL                  │
└─────────────────────────────────────────────────────────┘
``` 

## 🎓 Conceitos Fundamentais Aplicados

### 1. 🔄 API REST (Representational State Transfer)

**O que é?**  
API REST é um estilo arquitetural para projetar sistemas web que seguem os princípios da web.

**Por que usamos?**
- Separa o **frontend** (interface) do **backend** (lógica)
- Permite que múltiplos clientes (web, mobile, desktop) usem a mesma API
- Comunicação padronizada via HTTP e JSON

**Exemplo prático no projeto:**
```javascript
// Requisição para buscar produtos
GET /api/products/?category=1&min_price=100

// Resposta em JSON
{
  "count": 5,
  "results": [
    {"id": 1, "name": "Notebook", "price": 3500.00},
    {"id": 2, "name": "Mouse", "price": 50.00}
  ]
}
```
### 2. 📦 Serialização (Object → JSON)
O que é?
Processo de converter objetos complexos (Python/Model) em formato simples (JSON) que pode ser transmitido pela web.

Por que é necessário?

Navegadores entendem JSON, não objetos Python

JSON é leve e universal

Permite comunicação entre diferentes sistemas

**Implementação no projeto:**
```
# Modelo Python
product = Products.objects.get(id=1)
# <Product: Notebook Dell>

# Serializador
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'price']

# JSON gerado
{
    "id": 1,
    "name": "Notebook Dell",
    "price": "3500.00"
}

````

### 3. 🛡️ Django ORM e Segurança
O que é ORM?
Object-Relational Mapping - Técnica que mapeia tabelas do banco de dados para objetos Python.

Vantagens:

Proteção automática contra SQL Injection (principal benefício)

Código mais limpo e legível

Banco de dados independente (SQLite, PostgreSQL, MySQL)

**Exemplo de Proteção:**
```
# ❌ Vulnerável a SQL Injection (NUNCA fazer)
nome = request.GET.get('nome')
query = f"SELECT * FROM products WHERE name LIKE '%{nome}%'"
cursor.execute(query)  # PERIGO!

# ✅ Seguro - Django ORM
nome = request.GET.get('nome')
products = Products.objects.filter(name__icontains=nome)
# Django escapa automaticamente caracteres especiais
```
### 4. 🔍 Parâmetros GET para Busca
O que são?
Dados enviados na URL para filtrar ou personalizar respostas.

Exemplos no projeto:
```
/api/products/                    # Todos produtos
/api/products/?category=1         # Filtra por categoria
/api/products/?min_price=100      # Preço mínimo
/api/products/?search=notebook    # Busca por nome
/api/products/?ordering=-price    # Ordena por preço decrescente
```
Vantagens:
```
✅ Cacheável - Pode ser armazenado em CDN/navegador

✅ Compartilhável - URLs podem ser salvas como favoritos

✅ Bookmarkável - Mantém os filtros ao favoritar

✅ Sem impacto no servidor - Requisição leve
```
### 5. 📝 DTO (Data Transfer Object) com Serializers
O que é?
Padrão de projeto que define como os dados devem ser transferidos entre sistemas.

**Aplicação:**
```
# Definindo quais campos serão expostos na API
class ProductListSerializer(serializers.ModelSerializer):
    """Versão LEVE do produto - para listagens"""
    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'image']
        # ⚠️ Descrição não é incluída para economizar banda

class ProductDetailSerializer(serializers.ModelSerializer):
    """Versão COMPLETA - para página de detalhes"""
    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'price', 'image', 'reviews']
        # ✅ Inclui todos os campos detalhados
```


## 🧪 Plano de Testes

### Metodologia

Os testes foram realizados seguindo as seguintes categorias:

| Tipo de Teste | Descrição | Ferramenta |
|---------------|-----------|------------|
| **Teste de Unidade** | Verifica componentes isolados (models, serializers) | Django TestCase |
| **Teste de Integração** | Verifica interação entre componentes (views, APIs) | Django TestClient |
| **Teste Funcional** | Verifica fluxos completos (compra, cadastro) | Selenium (simulado) |
| **Teste de API** | Verifica endpoints REST | Postman/DRF Browsable API |
| **Teste de Segurança** | Verifica SQL Injection, XSS | Testes manuais |

---

### 🎯 Cenários de Teste Implementados

#### 1. Testes de Produtos

| ID | Cenário | Entrada | Resultado Esperado | Status |
|----|---------|---------|-------------------|--------|
| P001 | Buscar produto por nome | `?q=notebook` | Retornar produtos com "notebook" no nome | ✅ OK |
| P002 | Buscar por categoria | `?category=1` | Retornar apenas produtos da categoria 1 | ✅ OK |
| P003 | Buscar por faixa de preço | `?min_price=100&max_price=500` | Produtos entre R$100 e R$500 | ✅ OK |
| P004 | Buscar sem resultados | `?q=produtoinexistente123` | Retornar lista vazia | ✅ OK |
| P005 | Busca com menos de 2 caracteres | `?q=a` | Mensagem "Digite pelo menos 2 caracteres" | ✅ OK |
| P006 | Acessar produto com slug inválido | `/produto/slug-invalido/` | Página 404 (não encontrado) | ✅ OK |
| P007 | Adicionar avaliação sem login | POST `/api/reviews/` | Status 401 (não autorizado) | ✅ OK |
| P008 | Adicionar avaliação com sucesso | POST com rate=5 | Status 201 (criado) | ✅ OK |

#### 2. Testes de Carrinho

| ID | Cenário | Entrada | Resultado Esperado | Status |
|----|---------|---------|-------------------|--------|
| C001 | Adicionar produto ao carrinho | `product_id=1, quantity=2` | Carrinho atualizado com 2 itens | ✅ OK |
| C002 | Adicionar produto duplicado | Mesmo produto duas vezes | Quantidade acumulada (2+3=5) | ✅ OK |
| C003 | Remover item do carrinho | DELETE `/cart/item/1/` | Item removido do carrinho | ✅ OK |
| C004 | Atualizar quantidade | `quantity=5` | Quantidade alterada para 5 | ✅ OK |
| C005 | Carrinho vazio | Nenhum produto | Total = 0, itens = 0 | ✅ OK |
| C006 | Calcular total do carrinho | 2 produtos de R$50 | Total = R$100 | ✅ OK |

#### 3. Testes de Pedidos

| ID | Cenário | Entrada | Resultado Esperado | Status |
|----|---------|---------|-------------------|--------|
| O001 | Criar pedido com carrinho vazio | POST `/orders/create/` | Erro "Carrinho vazio" | ✅ OK |
| O002 | Criar pedido com sucesso | Dados de endereço completos | Pedido criado, carrinho limpo | ✅ OK |
| O003 | Listar pedidos do usuário | GET `/orders/` | Lista de pedidos do usuário logado | ✅ OK |
| O004 | Ver detalhes do pedido | GET `/orders/1/` | Dados completos do pedido | ✅ OK |

#### 4. Testes de Autenticação

| ID | Cenário | Entrada | Resultado Esperado | Status |
|----|---------|---------|-------------------|--------|
| A001 | Login com credenciais válidas | username/password corretos | Redirecionado para home | ✅ OK |
| A002 | Login com senha errada | username correto, senha errada | Mensagem de erro | ✅ OK |
| A003 | Registrar novo usuário | Dados válidos | Conta criada, redirecionado | ✅ OK |
| A004 | Registrar com email duplicado | Email já existente | Mensagem "Email já cadastrado" | ✅ OK |
| A005 | Acessar página de perfil sem login | GET `/profile/` | Redirecionado para login | ✅ OK |

#### 5. Testes de Segurança

| ID | Cenário | Entrada Maliciosa | Resultado Esperado | Status |
|----|---------|-------------------|-------------------|--------|
| S001 | SQL Injection na busca | `?q=' OR '1'='1` | Tratado como texto, não como SQL | ✅ OK |
| S002 | XSS (Cross-site Scripting) | `<script>alert('xss')</script>` | Caracteres escapados | ✅ OK |
| S003 | Acesso direto a arquivos | GET `/media/.env` | Acesso negado | ✅ OK |

---

### 🛠️ Como Executar os Testes

#### Testes Automatizados (Django)

```bash
# Executar todos os testes
python manage.py test

# Executar testes de um app específico
python manage.py test products
python manage.py test carts
python manage.py test orders

# Executar com verbosidade (mostra mais detalhes)
python manage.py test --verbosity=2

# Executar um teste específico
python manage.py test products.tests.ProductTestCase.test_search_product
```


🚀 Como Executar o Projeto

**Pré-requisitos**
```
-Python 3.11 ou superior

-Git

-Virtualenv (recomendado)
```

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/netosarmento/Projeto-Django-E-commerce.git
cd Projeto-Django-E-commerce

# 2. Crie e ative o ambiente virtual
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute as migrações (cria o banco de dados)
python manage.py migrate

# 5. Crie um superusuário (acesso ao admin)
python manage.py createsuperuser

# 6. Inicie o servidor de desenvolvimento
python manage.py runserver

# 7. Acesse no navegador

# Site: http://127.0.0.1:8000/
# Admin: http://127.0.0.1:8000/admin/
# API: http://127.0.0.1:8000/api/
```

**Comandos de Criação do Projeto:**

# Criar o projeto
```bash
django-admin startproject Project
```
# Criar os apps
```bash
python manage.py startapp products      # Produtos e categorias
python manage.py startapp orders        # Pedidos
python manage.py startapp users         # Perfil de usuários
python manage.py startapp carts         # Carrinho de compras
python manage.py startapp api           # API centralizada
```


## 📚 Referências e Recursos

### Documentação Oficial

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Python Official Docs](https://docs.python.org/)

### Conceitos Teóricos

- [REST APIs - Fielding, Roy (2000)](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
- [DTO Pattern - Fowler, Martin](https://martinfowler.com/eaaCatalog/dataTransferObject.html)
- [ORM Concepts - Ambler, Scott](https://www.agiledata.org/essays/mappingObjects.html)

### Ferramentas Utilizadas

- [Git](https://git-scm.com/)
- [GitHub](https://github.com/)
- [VS Code](https://code.visualstudio.com/)
- [Bootstrap 4](https://getbootstrap.com/docs/4.6/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.3/)
- [Font Awesome](https://fontawesome.com/icons)

### Conceitos Teóricos
REST APIs - Fielding, Roy (2000)

DTO Pattern - Fowler, Martin (2002)

ORM Concepts - Ambler, Scott (2004)

## 📞 Contato
```
Desenvolvedor: Carlos Jorge Sarmento Neto
GitHub: @netosarmento
Instagram: @norte_dev

```
## 📄 Licença

```
Projeto acadêmico - uso educacional permitido.
```
## 🙏 Agradecimentos
```
Professor Fábio Vidal, eo Professor Ennio pela orientação
```
## Colegas de turma pelas discussões técnicas

## Comunidade Django Brasil pelo suporte

## Desenvolvido com ❤️ para a Pós-Graduação em Desenvolvimento de Sistemas- IFTO
