import os
import re

from piwho import recognition

speakers = ['kait', 'courtney']


def train():
    """
    trains data on our model
    :return: no return value
    """
    speakers_file = "./speakers.txt"
    try:
        os.remove(speakers_file)
    except OSError as e:
        print("Error: " + str(e))
    for f in os.listdir('./'):
        if re.search('marf*', f):
            os.remove(os.path.join('./', f))

    name_list = speakers
    folder_path = './train_data/'
    recog = recognition.SpeakerRecognizer()
    recog.debug = True

    # setting classifier
    recog.set_feature_option('-noise -raw -aggr -eucl')
    for i in range(len(name_list)):
        recog.speaker_name = name_list[i]
        path = os.path.join(folder_path, name_list[i])
        print("Speaker Name: {} speaker_data: {}".format(name_list[i], name_list[i]))
        recog.train_new_data(path)


if __name__ == "__main__":
    train()