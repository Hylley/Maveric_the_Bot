from random import choice

def get_random(_list):
    if isinstance(_list[0], list):
        return choice(choice(_list))
    else:
        return choice(_list)


people = [
    'Harley',
    'Hylley',
    'Elon Musk',
    'Jair Messias Bolsonaro',
    'Luiz Inácio Lula da Silva',
    'Exército brasileiro',
    'meu professor de química',
    'Noosy',
    '007',
    'Cloud'
]

places = [
    'Universidade Federal do Estado de São Paulo',
    'minha casa'
]

adjectives = [
    'feio',
    'feia',
    'lindo',
    'linda',
    'gay',
    'hétero',
    'cringe'
]

substantives = [
    'anarcocapitalismo',
    'comunismo',
    'gatos',
    'pessoas',
    'homem',
    'feminismo',
    'Big Brother Brasil',
    'Linux',
    'Windows',
    'Google Meet',
    'YouTube',
    'quiasmo',
    'câncer',
    'sexo'
]

verbs = [
    'morrer',
    'sair'
]


structures = [
    f'{get_random(people)} vai entrar em uma batalha mortal com {get_random(people)}.',
    f'{get_random(people)} foi cancelado(a) por ser {get_random(adjectives)} de mais.',
    f'Imagina ter medo de {get_random([people, places, adjectives])}.',
    f'Eu odeio {get_random([people, places])} com todas as minhas forças.',
    f'Sem dúvidas {get_random([people, places])} foi a melhor coisa já criada.',
    'Vocês sabem como que',
    f'Como eu conto {get_random(people)} que eu secretamente gosto dele(a)?',
    f'Como eu conto aos meus pais que eu sou {get_random(adjectives)}?',
    f'{get_random(people)} é a pessoa mais {get_random(adjectives)} que eu já vi na vida.',
    f'Acho interessante que quanto mais {get_random(adjectives)} alguém é, mais {get_random(adjectives)} a mesma pessoa é.',
    f'Você prefere dinheiro ou {get_random([places, substantives])}?',
    f'Coisas para se fazer no Brasil: {get_random(verbs)}.'

]

def return_random_phrase():
    return choice(structures)