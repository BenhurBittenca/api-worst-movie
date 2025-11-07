# Golden Raspberry Awards API - Windows

Uma API RESTful em Python com FastAPI para gerenciar dados dos indicados e vencedores da categoria Pior Filme do Golden Raspberry Awards.

## 🛠 Pré-requisitos

- Python 3.8+ instalado
- PowerShell

## 🚀 Como Rodar

### 1. Abra o PowerShell no diretório do projeto

### 2. Crie o ambiente virtual
```powershell
python -m venv venv
```

### 3. Ative o ambiente virtual
```powershell
.\venv\Scripts\Activate.ps1
```
```cmd
.\venv\Scripts\activate.bat
```

### 4. Instale as dependências
```powershell
pip install -r requirements.txt
```

### 5. Execute a aplicação
```powershell
uvicorn app.main:app --reload
```

### 6. Acesse a API
- **API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs

## 🧪 Executar Testes

```powershell
python -m pytest tests/ -v
```

## 📊 Endpoints Principais

- **GET** `/movies/producer-intervals` - Retorna intervalos entre vitórias dos produtores
- **POST** `/movies/load-csv` - Recarrega dados do CSV
- **GET** `/health` - Verifica se a API está funcionando

## 🔧 Parar a Aplicação

Pressione `Ctrl + C` no terminal onde a aplicação está rodando.

## 🆘 Problemas Comuns

### Erro de execução de scripts PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Porta em uso
```powershell
uvicorn app.main:app --reload --port 8001
```

---
**Desenvolvido com FastAPI**

