# 📦 Sistema de Gestão de Estoque & Produtos

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Framework-Flask_3.0-black?logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow?logo=javascript&logoColor=black)
![Database](https://img.shields.io/badge/Database-SQLite%20%2F%20MySQL-blue?logo=sqlite&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-MVC-green)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

> **Projeto Integrador Transdisciplinar em Sistemas de Informação II (PIT-II)**  
> Aplicação web desenvolvida para controle centralizado de estoque, produtos e categorias, com foco em arquitetura limpa, usabilidade e comunicação assíncrona.

---

## 📌 Sumário
- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura MVC](#-arquitetura-mvc)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Como Executar Localmente](#-como-executar-localmente)
- [Rotas da API RESTful](#-rotas-da-api-restful)
- [Testes e Laudo de Qualidade](#-testes-e-laudo-de-qualidade)
- [Autora](#-autora)

---

## 🚀 Sobre o Projeto

O **Sistema de Gestão de Estoque e Produtos** foi desenvolvido como requisito prático da disciplina **PIT-II**. O sistema resolve problemas comuns de desorganização operacional e inconsistência em cadastros, oferecendo uma interface responsiva acoplada a uma API REST e banco de dados relacional.

---

## ✨ Funcionalidades

- [x] **CRUD Completo de Produtos:** Cadastro, listagem, atualização e exclusão de itens.
- [x] **Busca Dinâmica:** Filtro em tempo real por nome ou categoria sem necessidade de reload na página.
- [x] **Comunicação Assíncrona (AJAX):** Uso do JavaScript `fetch` API para consumo fluido das rotas.
- [x] **Validação em Camadas:** Bloqueio de preços nulos ou negativos e quantidade inválida no front-end e no back-end.
- [x] **Modal de Confirmação:** Interrupção de segurança para evitar exclusões acidentais de registros.
- [x] **Tratamento de Estado Vazio:** Feedback visual amigável quando a base de dados não possui produtos cadastrados.
- [x] **Auditoria:** Registro automático de data e hora de criação dos itens no banco de dados.

---

## 🏗️ Arquitetura MVC

A aplicação foi estruturada seguindo rigorosamente o padrão de arquitetura **Model-View-Controller**:

```text
               ┌───────────────────────┐
               │    Navegador (View)   │
               └───────────┬───────────┘
                           │  HTTP Request (Fetch)
                           ▼
               ┌───────────────────────┐
               │ Controller (Flask/Py) │
               └───────────┬───────────┘
                           │  Consultas SQL / Regras
                           ▼
               ┌───────────────────────┐
               │ Model (SQLite/MySQL)  │
               └───────────────────────┘
```

- **Model (`models/produto_model.py`):** Responsável pela persistência e consultas diretamente no banco de dados SQLite.
- **View (`templates/index.html` + `static/`):** Interface do usuário em HTML5, CSS3 responsivo e lógica client-side em JavaScript.
- **Controller (`controllers/produto_controller.py`):** Gerencia as requisições HTTP, rotas da API, sanitização e validação das regras de negócio.

---

## 🛠️ Tecnologias Utilizadas

- **Back-end:** Python 3.11+, Flask 3.0
- **Front-end:** HTML5, Tailwind CSS 3 via CDN, JavaScript ES6+ (Fetch API), Lucide e Toastify
- **Banco de Dados:** SQLite3 / MySQL
- **Gerenciamento de Dependências:** `pip`
- **Controle de Versão:** Git e GitHub

---

## 📂 Estrutura do Repositório

```text
PIT2-Sistema-de-Gestao/
│
├── app.py                      # Ponto de entrada e inicialização do Flask
├── requirements.txt            # Dependências do projeto
├── README.md                   # Documentação do repositório
│
├── models/                     # Camada MODEL (Persistência)
│   ├── __init__.py
│   └── produto_model.py
│
├── controllers/                # Camada CONTROLLER (Rotas e Regras)
│   ├── __init__.py
│   └── produto_controller.py
│
├── utils/                      # Utilitários compartilhados
│   └── api_response.py
│
├── static/                     # Arquivos Estáticos da View
│   └── js/
│       └── main.js
│
└── templates/                  # Camada VIEW (Interface HTML)
    └── index.html
```

---

## 💻 Como Executar Localmente

### Pré-requisitos
- **Python 3.8+** instalado na sua máquina.
- **Git** instalado.

### Passo a Passo

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/karinemenezes/PIT2-Sistema-de-Gestao.git
   cd PIT2-Sistema-de-Gestao
   ```

2. **Criar e ativar um ambiente virtual (Opcional, mas recomendado):**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Opcional) Configurar variáveis de ambiente:** crie um arquivo `.env` na raiz do projeto:
   ```dotenv
   PORT=5000
   FLASK_DEBUG=false
   DATABASE_PATH=database.db
   ```
   `DATABASE_PATH` pode receber um caminho absoluto ou relativo à pasta de execução. O arquivo `.env` não deve ser enviado ao Git.

5. **Executar a aplicação:**
   ```bash
   python app.py
   ```

6. **Acessar no navegador:**
   Abra seu navegador web e acesse `http://127.0.0.1:5000`.

---

## 🔌 Rotas da API RESTful

| Método | Endpoint | Descrição | Status HTTP |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | Renderiza a página principal (View) | `200 OK` |
| **GET** | `/api/produtos` | Retorna todos os produtos em JSON | `200 OK` |
| **POST** | `/api/produtos` | Cadastra um novo produto | `201 Created` / `400 Bad Request` |
| **DELETE** | `/api/produtos/<id>` | Deleta o produto pelo ID especificado | `200 OK` / `404 Not Found` |

As respostas JSON seguem o formato `{ "success": true, "data": {}, "message": "...", "timestamp": "..." }`.
Os valores de `data` variam conforme a rota; erros de validação e erros HTTP usam o mesmo envelope.

---

## 🧪 Testes e Laudo de Qualidade

O sistema passou por ciclos de testes de verificação e validação, incluindo avaliação de usabilidade realizada por 5 testadores. Principais correções aplicadas durante o ciclo:

1. **Validação de Preços:** Implementado bloqueio para valores negativos no front-end (`min="0.01"`) e back-end (`HTTP 400`).
2. **Confirmação de Deleção:** Adicionado prompt `confirm()` antes da exclusão de dados.
3. **Reset de Formulário:** Adicionado `form.reset()` imediato após submissão bem-sucedida.

---

## 👤 Autora

**Karine de Oliveira Menezes**  
Estudante de Sistemas de Informação  
[GitHub](https://github.com/karinemenezes) | [LinkedIn](https://linkedin.com)

---
*Projeto desenvolvido para a disciplina de Projeto Integrador Transdisciplinar em Sistemas de Informação II (PIT-II).*