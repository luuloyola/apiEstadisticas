from classes.message import Message
from classes.statistics import Statistics
from functions.models import get_message_analytics, get_llm_response
from functions.calculations import sum_amount_messages,max_words_per_message,min_words_per_message

def define_statistics(chat: list[Message]):
    print("entre a define statistics")
    sum = sum_amount_messages(chat)
    min = min_words_per_message(chat)
    max = max_words_per_message(chat)

    print("por obtener la respuesta del llm")
    llm_response = get_llm_response(chat)

    hateful_messages = 0
    ironic_messages = 0
    print("por obtener los valores de analytics sentiment")
    for message in chat:
        analytic = get_message_analytics(message.get_content())
        if analytic['hateful'] == 'hateful' or analytic['hateful'] == 'aggresive':
            hateful_messages += 1

        if analytic['irony'] == 'ironic':
            ironic_messages += 1

        message.set_sentiment(analytic['sentiment'])

    hate_percentage = hateful_messages/sum
    irony_percentage = ironic_messages/sum

    chat_statistics = Statistics(hate_percentage, irony_percentage, min, sum, llm_response.change_theme, llm_response.bet_type, llm_response.summary, chat[0].chat_id, max)
    print("por salir del principal")
    return chat_statistics, chat




