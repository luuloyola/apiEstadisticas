"""
API utilizada para el procesamiento de mensajes para el calculo de estadisticas

Estadisticas planteadas
- Resumen del chat: máximo de 280 caracteres.
- Tipo de apuesta: fútbol, juego clásico, etc
- Evolución de los sentimientos
- Utiliza lenguaje ofensivo: T o F
- Quiso cambiar el tema de conversación: T o F
- Tono irónico: T o F
"""
from datetime import time, datetime
from fastapi import FastAPI
from classes.message import Message
from db.connections import get_chat_session, transaction_stats
from functions.principal import define_statistics

app = FastAPI()
@app.post("/stats")
async def post_stats():
    list_session = get_chat_session()

    if list_session is None:
        return {"message": "No hay sesiones nuevas para procesar."}

    for session in list_session:
        try:
            stat, chat = define_statistics(session)
        except Exception as e:
            return{"message": "Se produjo un error interno. Error: %s"%e}

        try:
            transaction_stats(stat, chat)
            return {"message": "Se crearon las estadísticas correctamente"}
        except Exception as e:
            return{"message": "Se produjo un error interno. Error: %s"%e}