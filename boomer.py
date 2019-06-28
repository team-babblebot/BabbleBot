import random

prefix = [
'Look at you! ',
'Bless ',
'Bless! ',
'I heard about that! ',
'Amen!',
'You and the kids doing alright?',
'Miss ya\'ll!'
]

suffix = [
'. Amen!',
'. God bless america',
'. God bless!',
' haha'
'. love ya!'
'. love ya\'ll!'
]

def add_pre_suf(sentence):
    if random.randint(1,10) <= 6:
        if random.randint(1,10) <= 5:
            sentence = prefix[random.randint(0, len(prefix) - 1)] + sentence
        else:
            sentence += suffix[random.randint(0, len(suffix) - 1)]
    return sentence

def add_elipses(sentence):
    words = sentence.split()
    for i in range(4, len(words), 5):
        if random.randint(1,10) <= 7:
            words[i] += "..."
    return " ".join(words)

def boomer_caps(sentence):
    seed = random.randint(1, 10)
    sent_array = sentence.split()
    if seed in (1, 2, 3):
        return sentence
    elif seed in (4, 5):
        temp_sent = []
        for x in sent_array:
            if random.random() < 0.25:
                x = x.upper()
            temp_sent.append(x)
        return " ".join(temp_sent)
    elif seed in (6, 7):
        temp_sent = []
        for x in sent_array:
            if random.random() < 0.5:
                x = x.upper()
            temp_sent.append(x)
        return " ".join(temp_sent)
    elif seed in (8, 9):
        return sentence.title()
    elif seed == 10:
        return sentence.upper()
