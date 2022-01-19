import tweepy
# from dotenv import load_dotenv
import os
from boto.s3.connection import S3Connection

import tweetContentFilter


def twitterAuthenticate():
    # load_dotenv()

    # Autenticação.
    auth = tweepy.OAuthHandler(S3Connection(os.environ['API_KEY'], os.environ['API_KEY_SECRET']))
    auth.set_access_token(S3Connection(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET']))

    # Criação do objeito de API do Twitter.
    twt = tweepy.API(auth)
    return twt


def verifyForNewReplies(twitter_api):  # Verificação de novas respostas.
    latest_reply_id = tweetContentFilter.lastRegisteredReplyId()

    reply_list = twitter_api.mentions_timeline(
        since_id = (
            latest_reply_id
        ),
        tweet_mode = "extended"
    )

    for reply in reply_list:
        if tweetContentFilter.banWordsFilter(reply.full_text, reply.id):
            print("<--Ignorado. (Palavra banida)-->")
            reply_list.remove(reply)
        elif reply.full_text.endswith("$"):
            print("<--Ignorado. (Sufixo  $)-->")
            reply_list.remove(reply)

    return reply_list


def replyTweet(twitter_api_obj, content, in_reply_to_status_id):
    content = tweetContentFilter.linkMentionFilter(content)

    twitter_api_obj.update_status(status=content, in_reply_to_status_id=in_reply_to_status_id, auto_populate_reply_metadata=True)
    print('Response:', content)