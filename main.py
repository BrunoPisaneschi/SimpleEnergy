from fastapi import FastAPI

from api.view import api_router

# Inicialização do FastAPI
app = FastAPI(
    title="SimpleEnergy",
    description="API desenvolvida como desafio técnico para a SimpleEnergy.",
    version="1.0.0",
    redoc_url=None
)

app.include_router(api_router)
