# 🚀 Flask App - Rodando Localmente e com Docker

Bem-vindo ao projeto Flask mais estiloso da galáxia! 🌌 Se você quer rodar isso localmente como um guerreiro raiz ou dentro de um Docker como um mestre das nuvens, aqui está tudo o que você precisa saber. 👇

---

## 💻 Rodando Localmente

Se você gosta de rodar as coisas direto no seu ambiente, siga esses passos:

### 📌 Pré-requisitos
- Python 3.11 ou superior instalado 🐍
- Pip (gerenciador de pacotes do Python)

### 🔥 Como Rodar
1. Clone este repositório:
   ```sh
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```
2. Crie um ambiente virtual (opcional, mas recomendado):
   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```sh
   flask run
   ```
5. Acesse no navegador: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🐳 Rodando com Docker

Se você quer rodar isso de forma moderna e escalável, bora de Docker! 🏗️

### 📌 Pré-requisitos
- Docker instalado 🐳
- Docker Compose (opcional, mas recomendado)

### 🔥 Como Rodar com Docker Compose
1. Clone o repositório (caso ainda não tenha feito):
   ```sh
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```
2. Construa e rode o contêiner:
   ```sh
   docker-compose up --build
   ```
3. Acesse no navegador: [http://localhost:5000](http://localhost:5000)

### 🚀 Para rodar sem Docker Compose
Se você quiser rodar manualmente sem `docker-compose`, pode fazer assim:
   ```sh
   docker build -t flask-app .
   docker run -p 5000:5000 flask-app
   ```

---

## 🎯 Como Fazer Alterações no Código?
Se você está rodando localmente, basta editar os arquivos e reiniciar o Flask.

Se estiver rodando com **Docker Compose**, o código já está sincronizado (graças ao `volumes` no `docker-compose.yml`), então as alterações serão aplicadas automaticamente! 😎🔥

---

## 📢 Problemas?
Se algo der errado, respire fundo e cheque:
- O Docker está rodando?
- O Python está instalado corretamente?
- Algum erro no terminal?

Se tudo mais falhar, pergunte para o pato de borracha 🦆 ou me chame! 😆

---

Agora, divirta-se programando! 🚀🔥

