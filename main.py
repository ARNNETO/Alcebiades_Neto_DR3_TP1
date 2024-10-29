from fastapi import FastAPI
from routes import router  # Importando o router do arquivo routes.py

app = FastAPI()

# Incluindo as rotas do arquivo routes.py
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
