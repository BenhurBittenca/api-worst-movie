# Golden Raspberry Awards API

Uma API RESTful desenvolvida em Python com FastAPI para gerenciar dados dos indicados e vencedores da categoria Pior Filme do Golden Raspberry Awards.

## 📋 Guias de Instalação por Sistema Operacional

- **Windows**: [README-Windows.md](README-Windows.md)
- **Linux/Mac**: [README-Linux-Mac.md](README-Linux-Mac.md)

## 🛠 Tecnologias Utilizadas

- **FastAPI**: Framework web moderno para construção de APIs
- **SQLAlchemy**: ORM para gerenciamento de banco de dados
- **SQLite**: Banco de dados em memória para desenvolvimento
- **Pandas**: Manipulação e análise de dados CSV
- **Pytest**: Framework de testes
- **Uvicorn**: Servidor ASGI para produção

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes do Python)

## 🚀 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone <repository-url>
cd golden-raspberry-awards-api
```

### 2. Crie e ative o ambiente virtual

**No Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**No Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Execute a aplicação
```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## 📁 Estrutura do Projeto

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Configuração principal da aplicação
│   ├── database.py          # Configuração do banco de dados
│   ├── models.py            # Modelos SQLAlchemy
│   ├── services.py          # Lógica de negócio
│   └── routers/
│       ├── __init__.py
│       └── movies.py        # Endpoints da API
├── tests/
│   ├── __init__.py
│   └── test_integration.py  # Testes de integração
├── movielist.csv            # Dados dos filmes
├── requirements.txt         # Dependências do projeto
└── README.md               # Este arquivo
```

## 🔌 Endpoints da API

### GET `/`
Endpoint raiz com informações básicas da API.

**Resposta:**
```json
{
  "message": "Golden Raspberry Awards API",
  "version": "1.0.0",
  "endpoints": {
    "producer_intervals": "/movies/producer-intervals",
    "load_csv": "/movies/load-csv (POST)",
    "docs": "/docs"
  }
}
```

### GET `/movies/producer-intervals`
Retorna os produtores com menor e maior intervalo entre vitórias consecutivas.

**Resposta:**
```json
{
  "min": [
    {
      "producer": "Joel Silver",
      "interval": 1,
      "previousWin": 1990,
      "followingWin": 1991
    }
  ],
  "max": [
    {
      "producer": "Matthew Vaughn",
      "interval": 13,
      "previousWin": 2002,
      "followingWin": 2015
    }
  ]
}
```

### POST `/movies/load-csv`
Carrega dados do arquivo CSV para o banco de dados.

**Resposta:**
```json
{
  "message": "CSV data loaded successfully"
}
```

### GET `/health`
Endpoint de verificação de saúde da API.

**Resposta:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

## 📊 Formato do CSV

O arquivo `movielist.csv` deve seguir o formato:

```csv
year;title;studios;producers;winner
1980;Can't Stop the Music;Associated Film Distribution;Allan Carr;yes
1980;Cruising;Lorimar Productions, United Artists;Jerry Weintraub;
```

**Campos:**
- `year`: Ano do filme (inteiro)
- `title`: Título do filme (string)
- `studios`: Estúdios produtores (string)
- `producers`: Produtores (string, separados por vírgula e/ou " and ")
- `winner`: Vencedor ("yes" para verdadeiro, qualquer outra coisa para falso)

## 🧪 Executando os Testes

### Executar todos os testes
```bash
pytest tests/ -v
```

### Executar testes específicos
```bash
pytest tests/test_integration.py::test_producer_intervals_endpoint -v
```

### Executar testes com saída detalhada
```bash
pytest tests/ -v -s
```

## 📖 Documentação Interativa

Após iniciar a aplicação, acesse:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🌐 Exemplos de Uso

### Usando curl

#### Obter intervalos dos produtores
```bash
curl http://localhost:8000/movies/producer-intervals
```

#### Recarregar dados do CSV
```bash
curl -X POST http://localhost:8000/movies/load-csv
```

#### Verificar saúde da API
```bash
curl http://localhost:8000/health
```

### Usando Python requests
```python
import requests

# Obter intervalos dos produtores
response = requests.get("http://localhost:8000/movies/producer-intervals")
data = response.json()
print(data)

# Recarregar dados
response = requests.post("http://localhost:8000/movies/load-csv")
print(response.json())
```

## 🔧 Desenvolvimento

### Estrutura do Banco de Dados

A aplicação utiliza SQLite em memória com a seguinte estrutura:

**Tabela: movies**
- `id`: Chave primária (auto incremento)
- `year`: Ano do filme
- `title`: Título do filme
- `studios`: Estúdios
- `producers`: Produtores
- `winner`: Booleano indicando se foi vencedor
- `created_at`: Data/hora de criação

### Lógica de Negócio

A função principal `get_producer_intervals()` implementa:

1. Busca apenas filmes vencedores
2. Separa produtores múltiplos (vírgula e "and")
3. Calcula intervalos entre vitórias consecutivas
4. Identifica menor e maior intervalo
5. Retorna produtores com esses intervalos

### Carregamento de Dados

- Dados são carregados automaticamente na inicialização
- CSV usa separador ponto e vírgula (;)
- Campo "winner" com "yes" = True, outros valores = False
- Dados podem ser recarregados via endpoint POST

## 🐛 Solução de Problemas

### Erro ao carregar CSV
- Verifique se o arquivo `movielist.csv` existe na raiz do projeto
- Confirme que o separador é ponto e vírgula (;)
- Verifique a codificação do arquivo (UTF-8)

### Erro de dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Porta em uso
```bash
uvicorn app.main:app --reload --port 8001
```

## 📝 Notas de Desenvolvimento

- O código foi desenvolvido com foco na legibilidade e simplicidade
- Utiliza estruturas básicas do Python para facilitar manutenção
- Inclui logs detalhados para debugging
- Tratamento de erros básico implementado
- Testes abrangentes para validação

## 📄 Licença

Este projeto é desenvolvido para fins educacionais e de demonstração.

---
