import random


def fun_facts_helper():
    """
    Selects a random line from the fun fact responses
    :return: Fact string
    """

    resp = open('response_phrases/fun_facts.txt')
    line = next(resp)
    for num, aline in enumerate(resp):
        if random.randrange(num + 2):
            continue
        if aline != '':
            line = aline
        else:
            line = 'Dolphins sleep with one eye open'
    return line
