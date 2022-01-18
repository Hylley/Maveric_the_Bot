from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer

def clearBot(bot):  # Apaga o banco de dados do bot.
    bot.storage.drop()
    print("Clear.")


def trainCorpus(bot):  # Treina o bot em português.
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train('chatterbot.corpus.portuguese')
    print("Trained.")

def getResponse(bot, user_input):
    print('Request:', user_input)
    return bot.get_response(Statement(text=user_input, search_text=user_input))
