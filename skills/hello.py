import random


def hello_helper():
    """
    Selects a random line from the hello responses
    :return: Greeting string
    """

    resp = open('response_phrases/hello.txt')
    line = next(resp)
    for num, aline in enumerate(resp):
        if random.randrange(num + 2):
            continue
        if aline != '':
            line = aline
        else:
            line = 'Hello'
    return line


if __name__ == "__main__":
    hello_helper()
