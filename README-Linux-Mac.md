# Golden Raspberry Awards API - Linux/Mac

Uma API RESTful em Python com FastAPI para gerenciar dados dos indicados e vencedores da categoria Pior Filme do Golden Raspberry Awards.

## 🛠 Pré-requisitos

- Python 3.8+ instalado
- Terminal

## 🚀 Como Rodar

### 1. Abra o terminal no diretório do projeto

### 2. Crie o ambiente virtual
```bash
python3 -m venv venv
```

### 3. Ative o ambiente virtual
```bash
source venv/bin/activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Execute a aplicação
```bash
uvicorn app.main:app --reload
```

### 6. Acesse a API
- **API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs

## 🧪 Executar Testes

```bash
python -m pytest tests/ -v
```

## 📊 Endpoints Principais

- **GET** `/movies/producer-intervals` - Retorna intervalos entre vitórias dos produtores
- **POST** `/movies/load-csv` - Recarrega dados do CSV
- **GET** `/health` - Verifica se a API está funcionando

## 🔧 Parar a Aplicação

Pressione `Ctrl + C` no terminal onde a aplicação está rodando.

## 🆘 Problemas Comuns

### Porta em uso
```bash
uvicorn app.main:app --reload --port 8001
```

### Problemas de permissão (se necessário)
```bash
sudo python3 -m venv venv
```

---
**Desenvolvido com FastAPI**

