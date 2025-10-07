from classes.message import Message

def sum_amount_messages(chat: list[Message]) -> int:
    return len(chat)

def min_words_per_message(chat: list[Message]):
    min_words = len(chat[0].get_content().split())
    for message in chat:
        cant_palabras = len(message.get_content().split())
        if cant_palabras < min_words:
            min_words = cant_palabras
    return min_words

def max_words_per_message(chat: list[Message]):
    max_words = len(chat[0].get_content().split())
    for message in chat:
        cant_palabras = len(message.get_content().split())
        if cant_palabras > max_words:
            max_words = cant_palabras
    return max_words
