import json
import random

BEGIN_TAG = "<START>"
END_TAG = "<END>"
DEFAULT_STATE_LEN = 1

def get_zip(words, state_len: int =DEFAULT_STATE_LEN):
    zip_list = []
    for i in range(0, state_len + 1):
        zip_list.append(words[i:])
    return zip_list

def create_markov_model(corpus: str, delim: str = "\n", state_len: int =DEFAULT_STATE_LEN):
    model = {}

    for line in corpus.split(delim):
        # Split the sentence into words. Pad with a beginning and end tag.
        words = line.split()
        words.insert(0, BEGIN_TAG)
        words.append(END_TAG)

        # For every consecutive state_len + 1 words in the sentence, create or update a key/pair value.
        for tup in zip(*get_zip(words, state_len)):
            key = " ".join(tup[:-1])
            if key not in model:
                model[key] = []
            model[key] += [tup[-1]]

    return model

def gen_sentence(model, state_len: int =DEFAULT_STATE_LEN):
    sentence = []
    while not sentence:
        if state_len > 1:
            sentence = random.choice([key for key in model if key.split()[0] == BEGIN_TAG]).split()
        else:
            sentence = [random.choice(model[BEGIN_TAG])]

        while True:
            try:
                if state_len > 1:
                    curr_word = random.choice(model[" ".join(sentence[-state_len:])])
                else:
                    curr_word = random.choice(model[sentence[-1]])
            except KeyError:
                break
            if curr_word != END_TAG:
                sentence.append(curr_word)
            else:
                break
        if sentence[-1] == END_TAG:
            sentence = []
    if state_len > 1:
        sentence.pop(0)
    return " ".join(sentence)

if __name__ == "__main__":
    with open("197937757954375680.out", "r") as f:
        content = f.read()
    model = create_markov_model(content)
    for _ in range(10):
        print(gen_sentence(model))
    with open('vidata.json', 'w', encoding='utf-8-sig') as f:
        json.dump(model, f)

