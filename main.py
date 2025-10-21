import secrets

from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from db.connections import get_chat_session, transaction_stats
from functions.principal import define_statistics
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:8080",
    "https://novamas.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

load_dotenv()

VALID_TOKEN = os.getenv("ACCESS_TOKEN")


def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Usar Bearer token")
    except:
        raise HTTPException(status_code=401, detail="Formato inválido")

    if not VALID_TOKEN or not secrets.compare_digest(token, VALID_TOKEN):
        raise HTTPException(status_code=401, detail="No autorizado")

    return True


@app.post("/stats")
async def post_stats(authorized: bool = Depends(verify_token)):
    print("Entre a la API")
    list_session = await get_chat_session()

    if not list_session:
        raise HTTPException(status_code=204, detail="No hay sesiones nuevas para procesar.")

    errors = []
    for chat_session_id, session in list_session.items():
        try:
            stat, chat = define_statistics(session)
            transaction_stats(stat, chat)
        except Exception as e:
            errors.append(f"Error en sesión {chat_session_id}: {e}")

    if errors:
        raise HTTPException(status_code=500, detail={"errors": errors})

    return {"message": "Se crearon las estadísticas correctamente"}
