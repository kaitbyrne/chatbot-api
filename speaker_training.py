from piwho import recognition
from piwho import vad


def train_speaker(speaker_name):
    recog = recognition.SpeakerRecognizer()
    recog.speaker_name = speaker_name

    # Record audio until silence is detected
    # save WAV file
    vad.record()

    # train model with the newly recorded file
    recog.train_new_data()


if __name__ == '__main__':

    for i in range(0, 10):
        train_speaker('Kait')