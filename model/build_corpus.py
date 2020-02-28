import os


def build_corpus():
    """
    Combine all the training phrases into a large corpus to build a language model from
    Load corpus.txt into http://www.speech.cs.cmu.edu/tools/lmtool-new.html
    :returns: writes corpus.txt file
    """
    corpus_path = "corpus.txt"

    with open(corpus_path, "r+") as corpus:
        corpus_lines = set(corpus.read().splitlines())

        phrases_path = "../training_phrases"
        for filename in os.listdir(phrases_path):
            if filename.endswith('.txt'):
                phrase_file = "{}/{}".format(phrases_path, filename)

                with open(phrase_file) as f:
                    for line in f:
                        if line.strip('\n') not in corpus_lines:
                            print("{} -> Not in current corpus".format(line.strip('\n')))
                            corpus.write(line)


if __name__ == '__main__':
    build_corpus()
