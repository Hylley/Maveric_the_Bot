import tweepy
from dotenv import load_dotenv
import os
from codeLoop import every
import threading
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from time import sleep

from chatterbot.trainers import ChatterBotCorpusTrainer

def twitterAuthenticate():
    load_dotenv()

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    # Create API object
    twt = tweepy.API(auth)
    return twt


def replyTweet(twt, reply_status, bot):
    print(reply_status.text.replace('@MavericTheBot ', ''))
    response = bot.get_response(Statement(text = reply_status.text.replace('@MavericTheBot ', ''), search_text = reply_status.text.replace('@MavericTheBot ', '')))

    twt.update_status(response, in_reply_to_status_id=reply_status.id, auto_populate_reply_metadata=True)
    print(response)

def clearBot(bot):
    bot.storage.drop()
    print("Clear.")


def trainCorpus(bot):
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train('chatterbot.corpus.portuguese')
    print("Trained.")


# Main
twitter_api = twitterAuthenticate()
chatBot = ChatBot('Maveric')

reply_list = []


def verifyForNewReplies():
    latest_reply_id_txt = open('data_config/lastRegisteredReply.txt', 'r')
    latest_reply_id = latest_reply_id_txt.read()

    global reply_list

    reply_list = twitter_api.mentions_timeline(
        since_id=(
            latest_reply_id
        )
    )

    latest_reply_id_txt.close()
    postBotResponse()


def postBotResponse():
    if reply_list:
        for i in reply_list:
            last_registered_reply_txt = open('data_config/lastRegisteredReply.txt', 'w')
            last_registered_reply_txt.write(str(i.id))
            last_registered_reply_txt.close()

            replyTweet(twitter_api, i, chatBot)

            sleep(10)


verifyForNewReplies()
threading.Thread(target=lambda: every(60, verifyForNewReplies)).start()  # Creates a loop that search for new replies every 5 seconds.
