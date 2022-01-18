import tweepy
from dotenv import load_dotenv
import os
import io
from codeLoop import every
import threading
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from time import sleep
from chatterbot.trainers import ChatterBotCorpusTrainer


def twitterAuthenticate():
    load_dotenv()

    # Autenticação.
    auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    # Criação do objeito de API do Twitter.
    twt = tweepy.API(auth)
    return twt


def replyTweet(twt, reply_status, bot):  # Responde os tweets.
    print(reply_status.text)
    response = bot.get_response(Statement(text=reply_status.text.replace('@MavericTheBot ', ''),
                                          search_text=reply_status.text.replace('@MavericTheBot ', '')))

    twt.update_status(response, in_reply_to_status_id=reply_status.id, auto_populate_reply_metadata=True)
    print(response)


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


def clearBot(bot):  # Apaga o banco de dados do bot.
    bot.storage.drop()
    print("Clear.")


def trainCorpus(bot):  # Treina o bot em português.
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train('chatterbot.corpus.portuguese')
    print("Trained.")


# Código principal.

twitter_api = twitterAuthenticate()
chatBot = ChatBot('Maveric')


def verifyForNewReplies():  # Verificação de novas respostas.
    latest_reply_id_txt = open('data_config/lastRegisteredReply.txt', 'r')  # Último tweet respondido é necessário para evitar que o bot responda o mesmo tweet de novo.
    latest_reply_id = latest_reply_id_txt.read()

    reply_list = twitter_api.mentions_timeline(
        since_id = (
            latest_reply_id
        )
    )

    latest_reply_id_txt.close()

    for reply in reply_list:
        if banWordsFilter(reply.text):
            print("<--Ignorado. (Palavra banida)-->")
            reply_list.remove(reply)
        elif reply.text.endswith("$"):
            print("<--Ignorado. (Sufixo  $)-->")
            reply_list.remove(reply)

    postBotResponse(reply_list)


def postBotResponse(reply_list):
    if reply_list:
        for i in reply_list:
            last_registered_reply_txt = open('data_config/lastRegisteredReply.txt', 'w')
            last_registered_reply_txt.write(str(i.id))
            last_registered_reply_txt.close()

            replyTweet(twitter_api, i, chatBot)

            sleep(5)  # Delay entre as respostas para evitar que o Twitter limite a API.


verifyForNewReplies()
threading.Thread(target=lambda: every(30, verifyForNewReplies)).start()  # Cria um timer para refazer a procura de novas respostas e impede que o código termine.