from classes.message import Message
from classes.statistics import Statistics
from functions.models import get_llm_response, get_message_sentiment
from functions.calculations import sum_amount_messages,max_words_per_message,min_words_per_message

def define_statistics(chat: list[Message]):
    print("entre a define statistics")
    total_messages = sum_amount_messages(chat)
    min_words = min_words_per_message(chat)
    max_words = max_words_per_message(chat)

    print("por obtener la respuesta del llm")
    llm_response = get_llm_response(chat)
    print(llm_response.summary)

    positive_messages = 0
    negative_messages = 0
    neutral_messages = 0
    print("por obtener los valores de analytics sentiment")
    for message in chat:
        sentiment = get_message_sentiment(message.get_content())
        match sentiment:
            case 'POS': positive_messages+=1
            case 'NEG': negative_messages+=1
            case 'NEU': neutral_messages+=1

        message.set_sentiment(sentiment)

    positive_percentage = positive_messages/total_messages
    negative_percentage = negative_messages/total_messages
    neutral_percentage = neutral_messages/total_messages

    chat_statistics = Statistics(llm_response.hate_speech, llm_response.ironic, min_words, total_messages, llm_response.change_theme, llm_response.bet_type, llm_response.summary, chat[0].chat_id, max_words, chat[0].chat_group_id, positive_percentage, negative_percentage, neutral_percentage)

    print("por salir del principal")
    return chat_statistics




