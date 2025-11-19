import os
import enum
from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from pysentimiento import create_analyzer
from google import genai
from google.genai import types
from dotenv import load_dotenv
from classes.message import Message
import json

# Analizadores de mensajes
sentiment_analyzer = create_analyzer(task="sentiment", lang="es")

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt = os.getenv("SYSTEM_PROMPT")

class BetType(enum.Enum):
    CASINO_PRESENCIAL = "Casino Presencial"
    CASINO_ONLINE = "Casino Online"
    DEPORTIVA = "Deportiva"
    LOTERIA = "Loteria"
    VIDEOJUEGO = "Videojuego"
    NO_ESPECIFICA = "No especifica"


class LlmResponse(BaseModel):
    summary: str = Field(description="Resumen del chat en máximo 400 caracteres")
    bet_type: str = Field(
        description="Tipo de apuesta (DEBE ser uno de estos valores exactos): Casino Presencial, Casino Online, Deportiva, Loteria, Videojuego, No especifica"
    )
    hate_speech: bool = Field(description="Si contiene discurso de odio")
    ironic: bool = Field(description="Si es irónico")
    change_theme: bool = Field(description="Si cambia de tema")


def get_llm_response(chat: list[Message]):
    messages_content = [m.get_content() for m in chat]
    if messages_content.__contains__(""):
        messages_content.remove("")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_schema=LlmResponse),
            contents=messages_content
        )

        print(response.text)

        try:
            data = LlmResponse.model_validate_json(response.text)
            return data
        except Exception as e:
            print("Error de parseo")
            return None
    except Exception as e:
        print(f"\nError al llamar a gemini: {e}")
        return None


def get_message_sentiment(message: str):
    return sentiment_analyzer.predict(message).output