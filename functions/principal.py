from classes.message import Message
from classes.statistics import Statistics
from functions.models import get_llm_response, get_message_sentiment
from functions.calculations import sum_amount_messages,max_words_per_message,min_words_per_message

def is_user(message: Message):
    return message.get_role()=="user"

def define_statistics(chat: list[Message]):
    chat_user_f = filter(is_user, chat)
    chat_user = list(chat_user_f)

    total_messages = sum_amount_messages(chat_user)
    min_words = min_words_per_message(chat_user)
    max_words = max_words_per_message(chat_user)

    llm_response = get_llm_response(chat)

    positive_messages = 0
    negative_messages = 0
    neutral_messages = 0
    for message in chat_user:
        sentiment = get_message_sentiment(message.get_content())
        match sentiment:
            case 'POS': positive_messages+=1
            case 'NEG': negative_messages+=1
            case 'NEU': neutral_messages+=1

        message.set_sentiment(sentiment)

    positive_percentage = positive_messages/total_messages
    negative_percentage = negative_messages/total_messages
    neutral_percentage = neutral_messages/total_messages

    if positive_percentage>=negative_percentage and positive_percentage>=neutral_percentage:
        most_frequent = "POS"
    elif negative_percentage>=neutral_percentage:
        most_frequent = "NEG"
    else:
        most_frequent = "NEU"

    chat_statistics = Statistics(llm_response.hate_speech, llm_response.ironic, min_words, total_messages, llm_response.change_theme, llm_response.bet_type, llm_response.summary, chat[0].chat_id, max_words, chat[0].chat_group_id, positive_percentage, negative_percentage, neutral_percentage, most_frequent)
    return chat_statistics, chat




