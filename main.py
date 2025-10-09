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

chat1 = [[1,'hola', 'me siento mal', 'quiero apostar todo al rojo', 'mi papa me va a retar'],
         [2,'hola', 'me siento bien pero mi amigo no', 'aposto todo a river y perdio', 'como lo ayudo'],
         [3,'quiero ver taylor swift', 'no apuesto me estan obligando a hacer esto'],
         [4,'hola como estas', 'sos tonto', 'me caes mal', 'voy a apostar igual no me importa'],
         [5,'hola', 'me siento pesimo', 'quiero dejar de apostar pero no puedo']]

def mock_messages():
    list_session = dict()
    for i in chat1:
        list_session[i[0]] = []
        for j in i:
            if type(j) is str:
                new_message = Message([j, i[0],j, datetime.now()])
                list_session[i[0]].append(new_message)

    return list_session

def mock_get():
    print("entre a mock")
    chats = mock_messages()
    stats = dict.fromkeys(chats.keys())
    for key in chats:
        print("estoy en el for de mock con chat numero ",key)
        #stats[key] =\
        define_statistics(chats[key])
    """for i in stats:
        for j in chats[i]:
            print(j)
        print(stats[i])"""

mock_get()
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