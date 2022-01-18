import tweepy
from dotenv import load_dotenv
import os

import tweetContentFilter


def twitterAuthenticate():
    load_dotenv()

    # Autenticação.
    auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    # Criação do objeito de API do Twitter.
    twt = tweepy.API(auth)
    return twt


def verifyForNewReplies(twitter_api):  # Verificação de novas respostas.
    latest_reply_id = tweetContentFilter.lastRegisteredReplyId()

    reply_list = twitter_api.mentions_timeline(
        since_id = (
            latest_reply_id
        )
    )

    for reply in reply_list:
        if tweetContentFilter.banWordsFilter(reply.text):
            print("<--Ignorado. (Palavra banida)-->")
            reply_list.remove(reply)
        elif reply.text.endswith("$"):
            print("<--Ignorado. (Sufixo  $)-->")
            reply_list.remove(reply)

    return reply_list


def replyTweet(twitter_api_obj, content, in_reply_to_status_id):
    twitter_api_obj.update_status(status=content, in_reply_to_status_id=in_reply_to_status_id, auto_populate_reply_metadata=True)
    print('Response:', content)