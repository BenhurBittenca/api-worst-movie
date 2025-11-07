# Prompt para Desenvolvimento da API - Golden Raspberry Awards

## Contexto
Preciso desenvolver uma API RESTful em Python com FastAPI para gerenciar dados dos indicados e vencedores da categoria Pior Filme do Golden Raspberry Awards.

## Estrutura do Projeto

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── services.py
│   └── routers/
│       └── movies.py
├── tests/
│   ├── __init__.py
│   └── test_integration.py
├── data/
│   └── movielist.csv
├── requirements.txt
└── README.md
```

## Passo 1: Configurar o ambiente e dependências

**Arquivo: requirements.txt**
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pytest==7.4.3
httpx==0.25.2
pandas==2.1.3
```

## Passo 2: Criar o modelo de dados (models.py)

Crie uma classe Movie com os campos:
- id (inteiro, chave primária, auto incremento)
- year (inteiro)
- title (string)
- studios (string)
- producers (string)
- winner (booleano)
- created_at (datetime, preenchido automaticamente)

**Exemplo de implementação:**
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    title = Column(String)
    studios = Column(String)
    producers = Column(String)
    winner = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    # func.now() do SQLAlchemy insere automaticamente a data/hora no momento da criação
```

Use SQLAlchemy de forma simples e direta.

## Passo 3: Configurar o banco de dados em memória (database.py)

- Use SQLite em memória (sqlite:///:memory:)
- Configure o engine e session do SQLAlchemy
- Crie uma função simples para inicializar as tabelas

## Passo 4: Implementar a lógica de negócio (services.py)

Implemente duas funções principais:

**1. load_csv_data()**
- Leia o arquivo CSV usando pandas
- O separador é ponto e vírgula (;)
- Converta "yes" para True e vazio para False no campo winner
- Insira os dados no banco usando um loop simples
- Adicione prints para debug (ex: "Carregando dados do CSV...")

**2. get_producer_intervals()**
Esta é a função mais importante. Implemente com clareza:

a) Busque apenas filmes vencedores (winner=True)
b) Separe produtores que aparecem com vírgula ou " and " 
   - Ex: "Producer 1, Producer 2 and Producer 3" = 3 produtores
c) Para cada produtor:
   - Liste todos os anos que ganhou (ordenado)
   - Calcule intervalos entre vitórias consecutivas
   - Use um dicionário simples para armazenar: {producer: [(year1, year2, interval)]}
d) Encontre o menor e maior intervalo
e) Retorne no formato especificado

**Dica:** Use estruturas básicas do Python (loops, dicionários, listas). Evite código muito "clever" ou otimizações complexas.

## Passo 5: Criar os endpoints (routers/movies.py)

**GET /movies/producer-intervals**
- Endpoint principal que retorna min e max intervals
- Chame a função get_producer_intervals()
- Retorne JSON no formato:
```json
{
  "min": [{"producer": "...", "interval": 1, "previousWin": 2008, "followingWin": 2009}],
  "max": [{"producer": "...", "interval": 10, "previousWin": 2000, "followingWin": 2010}]
}
```

**POST /movies/load-csv**
- Endpoint para carregar dados do CSV manualmente
- Limpe a tabela antes de carregar
- Retorne mensagem de sucesso com contagem de registros

## Passo 6: Configurar a aplicação principal (main.py)

```python
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import movies
from app.services import load_csv_data

app = FastAPI(title="Golden Raspberry Awards API")

@app.on_event("startup")
def startup_event():
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    # Carregar dados do CSV automaticamente
    load_csv_data()
    print("API iniciada e dados carregados!")

app.include_router(movies.router)

@app.get("/")
def read_root():
    return {"message": "Golden Raspberry Awards API"}
```

## Passo 7: Implementar testes de integração (test_integration.py)

Crie testes que validem:

**1. test_load_csv_data()**
- Verifique se os dados foram carregados
- Conte registros no banco
- Verifique alguns registros específicos conhecidos

**2. test_producer_intervals_endpoint()**
- Faça requisição GET para /movies/producer-intervals
- Valide estrutura da resposta (min e max arrays)
- Valide campos obrigatórios: producer, interval, previousWin, followingWin
- Verifique se min tem intervalo menor que max

**3. test_known_producer_scenario()**
- Baseado nos dados reais do CSV fornecido
- Valide produtores específicos que você sabe que aparecem múltiplas vezes
- Ex: Verificar se algum produtor com vitórias em anos conhecidos está correto

Use pytest com TestClient do FastAPI para fazer requisições reais.

## Passo 8: Criar README.md completo

Inclua:
- Descrição do projeto
- Tecnologias utilizadas
- Como instalar dependências
- Como rodar a aplicação
- Como executar os testes
- Exemplos de uso da API com curl
- Estrutura do projeto

## Observações Importantes

1. **Código Legível:** Use nomes descritivos de variáveis, adicione comentários explicativos em partes importantes
2. **KISS (Keep It Simple):** Prefira soluções diretas a patterns complexos
3. **Tratamento de Erros:** Adicione try-except básicos em operações críticas
4. **Logs:** Use print() para debug, facilitando apresentação ao vivo
5. **Separação de Produtores:** Atenção especial para produtores múltiplos no mesmo registro
6. **CSV:** O separador é ponto e vírgula (;) não vírgula
7. **Winner:** Apenas "yes" indica vencedor, qualquer outra coisa (vazio, "no") é False
8. **diretorio do arquivo** O arquivo encontra-se em C:\Repos\test_outserra\movielist.csv

## Formato do CSV
```
year;title;studios;producers;winner
1980;Can't Stop the Music;Associated Film Distribution;Allan Carr;yes
1980;Cruising;Lorimar Productions, United Artists;Jerry Weintraub;
```

## Exemplo de Resposta Esperada
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

## Comandos para Executar

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar aplicação
uvicorn app.main:app --reload

# Rodar testes
pytest tests/ -v

# Testar endpoint
curl http://localhost:8000/movies/producer-intervals
```

---

**Importante:** Desenvolva pensando que será apresentado ao vivo. O código deve ser fácil de entender, bem organizado e funcional. Evite over-engineering.