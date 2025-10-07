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
class Statistics:
    def __init__(self, hate, irony, min, sum, theme, bet, summary, chat_id, max):
        self.summary = summary
        self.chat_id = chat_id
        self.amount_messages = sum
        self.min_words_per_message = min
        self.max_words_per_message = max
        self.hate_speech_percentage = hate
        self.ironic_percentage = irony
        self.change_theme = theme
        self.bet_type = bet

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

    def set_ironic_percentage(self, ironic):
        self.ironic_percentage = ironic

    def set_hate_percentage(self, hate_speech):
        self.hate_speech_percentage = hate_speech

    def get_summary(self):
        return self.summary

    def get_chat_id(self):
        return self.chat_id

    def get_amount_messages(self):
        return self.amount_messages

    def get_min_words_per_message(self):
        return self.min_words_per_message

    def get_max_words_per_message(self):
        return self.max_words_per_message

    def get_hate_speech_percentage(self):
        return self.hate_speech_percentage

    def get_ironic_percentage(self):
        return self.ironic_percentage

    def get_change_theme(self):
        return self.change_theme

    def get_bet_type(self):
        return self.bet_type

    def __str__(self):
        return (
            f"📊 Estadísticas del Chat (ID: {self.chat_id})\n"
            f"- Resumen: {self.summary[:280]}{'...' if len(self.summary) > 280 else ''}\n"
            f"- Tipo de apuesta: {self.bet_type}\n"
            f"- Cantidad de mensajes: {self.amount_messages}\n"
            f"- Palabras por mensaje (mín): {self.min_words_per_message}\n"
            f"- Palabras por mensaje (máx): {self.max_words_per_message}\n"
            f"- Lenguaje ofensivo: {'T' if self.hate_speech_percentage > 0 else 'F'} "
            f"({self.hate_speech_percentage}%)\n"
            f"- Tono irónico: {'T' if self.ironic_percentage > 0 else 'F'} "
            f"({self.ironic_percentage}%)\n"
            f"- Cambio de tema: {'T' if self.change_theme else 'F'}"
        )