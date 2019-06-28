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