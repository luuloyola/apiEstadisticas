import os
import enum
from typing import Optional
from pydantic import BaseModel, Field
from pysentimiento import create_analyzer
from google import genai
from google.genai import types
from dotenv import load_dotenv
from classes.message import Message

# Analizadores de mensajes
sentiment_analyzer = create_analyzer(task="sentiment", lang="es")

# Mensajes de prueba
chat = [
    "Hola, necesito ayuda",
    "Aposte todo mi dinero a mi equipo de futbol favorito y perdi todo",
    "No se como decirselo a mis papas",
    "Ayudame loco",
    "Soy de san luis, con quien puedo hablar?",
    "Me llamo juana",
    "Mi numero de pasaporte es 233232"
    "Como esta el dia?",
    "Esta lloviendo?",
    "Como estara taylor swift? viste que se caso"
]
frase = ["Tengo un amigo gordo que es re puto y me cae mal",
         "Estoy re ocupado que no tengo casi tiempo",
         "Vas a llegar muy cerca!!",
         "si che? No te pregunté",
         "pobre de vos",
         "estoy en la luna",
         "no, en serio! sos un genio, nadie habia pensado en eso antes",
         "uy que sorpresa, justo lo que necesitaba",
         "La concha de tu madre",
         "La puta madre",
         "La concha de mi hermana",
         "La concha del loro",
         "pero vos sos estupido",
         "Claro, porque dejar todo para último momento siempre da excelentes resultados",
         "¿Reunión de una hora que podría haber sido un mail? ¡Increíble innovación!"
         ]

load_dotenv()
client = genai.Client()
system_prompt = os.getenv("SYSTEM_PROMPT")

class BetType(enum.Enum):
    CASINO_PRESENCIAL = "Casino Presencial"
    CASINO_ONLINE = "Casino Online"
    DEPORTIVA = "Deportiva"
    LOTERIA = "Loteria"
    VIDEOJUEGO = "Videojuego"
    NO_ESPECIFICA = "No especificado"

class LlmResponse(BaseModel):
    summary: str = Field(max_length=280)
    bet_type: Optional[BetType]
    change_theme: bool

def get_llm_response(chat: list[Message]):
    messages_content = []
    for m in chat:
        messages_content.append(m.get_content())

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_schema=LlmResponse),
        contents=messages_content
    )

    print(response.text)

    try:
        response_parsed: LlmResponse = response.parsed
        print("\nPRIMERO EL OBJETO COMPLETO\n")
        print(response_parsed)
        print("\nAHORA ES SUMMARY")
        print(response_parsed.summary)
        print()
        print(response_parsed.bet_type)
        print(response_parsed.change_theme)
        return response_parsed
    except Exception as e:
        print("Error al parsear:", e)
        print("Respuesta cruda:", response.text)


def get_message_analytics(message: str):
    analytics = dict.fromkeys(['sentiment'])
    analytics.update({'sentiment': sentiment_analyzer.predict(message).output})
    print(analytics)
    return analytics


"""
for f in frase:
    print("La frase es: ", f)
    print("\nIronia de roberta: \n")
    print(pipe_ironia(f))
    print("Ofensivo de roberta: \n")
    print(pipe(f))
    print("Emotion analyzer: \n")
    print(emotion_analyzer.predict(f))
    print("Sentiment analyzer: \n")
    print(sentiment_analyzer.predict(f))
    print("Irony analyzer: \n")
    print(irony_analyzer.predict(f))
    print("Hate analyzer: \n")
    print(hate_speech_analyzer.predict(f))
"""