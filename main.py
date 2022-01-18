from codeLoop import every
from time import sleep
import schedule

import twitterAPI
import botAI
import tweetContentFilter


twitter_api_obj = twitterAPI.twitterAuthenticate()
chatBot = botAI.ChatBot('Maveric')


def updateBot():
    reply_list = twitterAPI.verifyForNewReplies(twitter_api_obj)

    if reply_list:
        postBotResponse(twitter_api_obj, chatBot, reply_list)


def postBotResponse(twitter_api, chatBot, reply_list):
    if reply_list:
        for i in reply_list:
            replyTweet(twitter_api, i, chatBot)
            tweetContentFilter.updateLastReply(str(i.id))

            sleep(5)  # Delay entre as respostas para evitar que o Twitter limite a API.


def replyTweet(twt, reply_status, bot):  # Responde os tweets.
    bot_response = botAI.getResponse(bot, reply_status.text.replace('@MavericTheBot ', ''))
    twitterAPI.replyTweet(twt, content=bot_response, in_reply_to_status_id=reply_status.id)


updateBot()
schedule.every(30).seconds.do(updateBot)  # Cria um timer para refazer a procura de novas respostas e impede que o código termine.

while True:
    schedule.run_pending()
    sleep(1)