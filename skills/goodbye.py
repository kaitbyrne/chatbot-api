import random


def goodbye_helper():
    """
    Selects a random line from the goodbye responses
    :return: Goodbye string
    """

    resp = open('response_phrases/goodbye.txt')
    line = next(resp)
    for num, aline in enumerate(resp):
        if random.randrange(num + 2):
            continue
        if aline != '':
            line = aline
        else:
            line = 'Goodbye'
    return line


if __name__ == "__main__":
    goodbye_helper()
