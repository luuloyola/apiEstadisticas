from fastapi import FastAPI, HTTPException
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
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/stats")
async def post_stats():
    print("Entre a la API")
    list_session = get_chat_session()

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
