import io

data_config_folder = 'data_config/'

def updateLastReply(tweet_it):
    last_registered_reply_file = open(data_config_folder + 'lastRegisteredReply.txt', 'w')
    last_registered_reply_file.write(tweet_it)
    last_registered_reply_file.close()


def lastRegisteredReplyId():
    last_registered_reply_id_file = open(data_config_folder + 'lastRegisteredReply.txt', 'r')
    latest_reply_id = last_registered_reply_id_file.read()
    last_registered_reply_id_file.close()

    return latest_reply_id


def banWordsFilter(text):
    ban_dictionary = io.open('data_config/banDictionary.txt', mode = 'r', encoding="utf-8")
    ban_words = ban_dictionary.read()
    ban_dictionary.close()

    ban_word_allert = False

    for word in text.split():
        for ban_word in ban_words.split():
            if word.lower() == ban_word.lower():
                ban_word_allert = True

    return ban_word_allert