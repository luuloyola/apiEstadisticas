"""
Estadisticas
- Resumen del chat: máximo de 280 caracteres.
- Tipo de apuesta: fútbol, juego clásico, etc
- Cantidad de mensajes
- Minimo numero de palabras por mensaje
- Maximo numero de palabras por mensaje
- Utiliza lenguaje ofensivo: T o F
- Quiso cambiar el tema de conversación: T o F
- Tono irónico: T o F
"""
from functions.models import BetType
class Statistics:
    def __init__(self, hate, irony, min, sum, theme, bet, summary, chat_id, max, chat_group_id, positive_percentage, negative_percentage, neutral_percentage, most_frequent_sentiment):
        self.summary = summary
        self.chat_id = chat_id
        self.chat_group_id = chat_group_id
        self.amount_messages = sum
        self.min_words_per_message = min
        self.max_words_per_message = max
        self.hate_speech = hate
        self.ironic = irony
        self.positive_percentage = positive_percentage
        self.negative_percentage = negative_percentage
        self.neutral_percentage = neutral_percentage
        self.change_theme = theme
        self.bet_type = bet
        self.most_frequent_sentiment = most_frequent_sentiment

    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

    def set_summary(self, summary):
        self.summary = summary

    def set_bet_type(self, bet_type):
        self.bet_type = bet_type

    def set_change_theme(self, change_theme):
        self.change_theme = change_theme

    def set_amount_messages(self, amount_messages):
        self.amount_messages = amount_messages

    def set_min_words_per_message(self, min_words_per_message):
        self.min_words_per_message = min_words_per_message

    def set_max_words_per_message(self, max_words_per_message):
        self.max_words_per_message = max_words_per_message

    def set_ironic(self, ironic):
        self.ironic = ironic

    def set_hate(self, hate_speech):
        self.hate_speech = hate_speech

    def get_summary(self):
        return self.summary

    def get_most_frequent_sentiment(self):
        return self.most_frequent_sentiment

    def get_chat_id(self):
        return self.chat_id

    def get_chat_group_id(self):
        return self.chat_group_id

    def get_amount_messages(self):
        return self.amount_messages

    def get_min_words_per_message(self):
        return self.min_words_per_message

    def get_max_words_per_message(self):
        return self.max_words_per_message

    def get_hate_speech(self):
        return self.hate_speech

    def get_ironic(self):
        return self.ironic

    def get_positive_percentage(self):
        return self.positive_percentage

    def get_negative_percentage(self):
        return self.negative_percentage

    def get_neutral_percentage(self):
        return self.neutral_percentage

    def get_change_theme(self):
        return self.change_theme

    def get_bet_type(self):
        match self.bet_type:
            case "Loteria": return "LOTERIA"
            case "Deportiva": return "DEPORTIVA"
            case "Videojuego": return "VIDEOJUEGO"
            case "Casino Online": return "CASINO_ONLINE"
            case "Casino Presencial": return "CASINO_PRESENCIAL"
            case "No especifica": return "NO_ESPECIFICA"
        return "NO_ESPECIFICA"

    def __str__(self):
        return (
            f"📊 Estadísticas del Chat (ID: {self.chat_id}) (Grupo ID: {self.chat_group_id})\n"
            f"- Resumen: {self.summary}\n"
            f"- Tipo de apuesta: {self.bet_type}\n"
            f"- Sentimiento mas frecuente: {self.most_frequent_sentiment}\n"
            f"- Cantidad de mensajes: {self.amount_messages}\n"
            f"- Palabras por mensaje (mín): {self.min_words_per_message}\n"
            f"- Palabras por mensaje (máx): {self.max_words_per_message}\n"
            f"- Porcentaje de mensajes positivos: {self.positive_percentage}\n"
            f"- Porcentaje de mensajes negativas: {self.negative_percentage}\n"
            f"- Porcentaje de mensajes neutrales: {self.neutral_percentage}\n"
            f"- Lenguaje ofensivo: {'T' if self.hate_speech else 'F'}\n"
            f"- Tono irónico: {'T' if self.ironic else 'F'}\n"
            f"- Cambio de tema: {'T' if self.change_theme else 'F'}"
        )
