# 🛒 Django E-commerce API

> Projeto desenvolvido para a disciplina de Desenvolvimento Web  
> **Pós-Graduação em Desenvolvimento de Sistemas**

---

## 👨‍🏫 Professor
**Fabio Vidal**

## 👥 Equipe

| Nome | Papel |
|---|---|
| Carlos Jorge Sarmento Neto | Desenvolvedor |


---

## 📋 Sobre o Projeto

API RESTful para sistema de **E-commerce** desenvolvida com Django e Django REST Framework.  
Projeto acadêmico com foco em boas práticas de desenvolvimento, arquitetura de APIs e integração com sistemas externos.

### Funcionalidades planejadas

- [ ] CRUD de produtos
- [ ] CRUD de categorias
- [ ] Autenticação JWT
- [ ] Carrinho de compras
- [ ] Pedidos e checkout
- [ ] Pagamentos integrados (mock)
- [ ] Documentação automática com Swagger/DRF-YASG

---

## 🛠 Tecnologias utilizadas

- Python 3.11+
- Django 5.x
- Django REST Framework
- MySQL (ou SQLite para desenvolvimento)
- Simple JWT (autenticação)
- DRF-YASG (documentação)
- django-cors-headers

---

## 🚀 Como executar o projeto

### Pré-requisitos

- Python 3.11 ou superior
- Git
- Virtualenv (recomendado)

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/netosarmento/Projeto-Django-E-commerce.git
cd Projeto-Django-E-commerce

# 2. Crie o ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

# 6. Execute as migrações
python manage.py migrate

# 7. Crie um superusuário
python manage.py createsuperuser

# 8. Inicie o servidor
python manage.py runserver

# Passos iniciais executados na criação do projeto:

# Criar Projeto
django-admin startproject Project 

# Criar Apps
python manage.py startapp products
python manage.py startapp orders
python manage.py startapp users
python manage.py startapp carts
