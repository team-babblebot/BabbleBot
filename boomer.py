import random

def add_elipses(sentence):
    words = sentence.split()
    for i in range(4, len(words), 5):
        if random.randint(1,10) <= 7:
            words[i] += "..."
    return " ".join(words)