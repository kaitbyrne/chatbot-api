import random


def jokes_helper():
    """
    Selects a random line from the joke responses
    :return: Joke string
    """

    resp = open('response_phrases/jokes.txt')
    line = next(resp)
    for num, aline in enumerate(resp):
        if random.randrange(num + 2):
            continue
        if aline != '':
            line = aline
        else:
            line = 'I intend to live forever. So far, so good.'
    return line
