from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import movies
from app.services import load_csv_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize application on startup
    """
    print("Iniciando Golden Raspberry Awards API...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("Tabelas do banco de dados criadas!")
    
    # Load CSV data automatically
    try:
        load_csv_data()
        print("API iniciada e dados carregados com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar dados na inicialização: {e}")
        # Continue anyway, data can be loaded manually via endpoint
    
    yield

app = FastAPI(
    title="Golden Raspberry Awards API",
    description="API para gerenciar dados dos indicados e vencedores da categoria Pior Filme do Golden Raspberry Awards",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(movies.router)

@app.get("/")
def read_root():
    """
    Root endpoint
    """
    return {
        "message": "Golden Raspberry Awards API",
        "version": "1.0.0",
        "endpoints": {
            "producer_intervals": "/movies/producer-intervals",
            "load_csv": "/movies/load-csv (POST)",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "message": "API is running"}
