import pyaudio
import operator
import wave
from piwho import recognition
from pocketsphinx import *
from pocketsphinx.pocketsphinx import *
from model.model_enum import Model


class PocketSphinxListener(object):

    def __init__(self, model, debug=False):
        self.debug = debug

        current_dir = os.path.dirname(os.path.realpath(__file__))

        self.hmm = '{}/model/en-us'.format(current_dir)

        if model == Model.STANDARD.value:
            self.dic = '{}/model/language_files/8435.dic'.format(current_dir)
            self.lm = '{}/model/language_files/8435.lm'.format(current_dir)
        elif model == Model.KEYWORD.value:
            self.dic = '{}/model/language_files/5574.dic'.format(current_dir)
            self.lm = '{}/model/language_files/5574.lm'.format(current_dir)

        self.sample_rate = 44100.0
        self.sample_format = pyaudio.paInt16
        self.frames_per_buffer = 8192

        self.config = Decoder.default_config()
        self.config.set_string('-hmm', self.hmm)
        self.config.set_string('-dict', self.dic)
        self.config.set_string('-lm', self.lm)
        self.config.set_float('-kws_threshold', 1e-50)

        # comment out the following line to get debugging output from the decoder
        if not self.debug:
            self.config.set_string('-logfn', '/dev/null')

        self.config.set_string('-verbose', 'yes')
        self.config.set_string('-logfn', 'psphinx.log')
        self.config.set_boolean("-allphone_ci", True)

        self.config.set_float('-samprate', self.sample_rate)
        self.config.set_int('-nfft', 2048)

        self.decoder = Decoder(self.config)

        # setting search for only keyword
        if model == Model.KEYWORD.value:
            self.decoder.set_keyphrase("keyword", "HEY RON")
            self.decoder.set_search('keyword')

    @staticmethod
    def print_results(scores_list):
        """
        function to print our first and second best speaker
        :param scores_list: list of speakers and scores
        :return: no return value
        """
        print("\nSpeaker identified: " + str(scores_list[0][0]))
        print("Second Best Guess: " + str(scores_list[1][0]) + "\n\n")

    @staticmethod
    def determine_speaker():
        """
        takes speaker input data from the microphone and determines who was speaking
        :return: a sorted list of scores for each team member from out distance classifier
        """
        recog = recognition.SpeakerRecognizer()

        # for now, set to classification by euclidean distance
        recog.set_feature_option('-noise -raw -aggr -eucl')
        name = recog.identify_speaker('./speak_detect.wav')
        print(name)
        scores = recog.get_speaker_scores()
        sorted_scores = {k: float(v) for k, v in scores.iteritems()}
        sort_s = sorted(sorted_scores.items(), key=operator.itemgetter(1))

        # print full dictionary of scores
        for k, v in sort_s:
            print("%s: %f" % (k, v))

        return sort_s

    @staticmethod
    def speaker_threshold(sorted_scores):
        """Function to determine if a speaker passes a certain threshold to determine if they are
        an authorized speaker
        :param sorted_scores: sorted list of team members and distance scores from closest to
        farthest
        """
        if not sorted_scores:
            return

        if sorted_scores[0][1] < 10.0:
            print("\nRecognized Speaker: {}\n".format(sorted_scores[0][0]))
        else:
            print("\nUnrecognized Speaker!\n")

    def check_speaker_recognition(self, ret_queue):
        """
        determine who was speaking to bot and see if they pass the threshold
        :param ret_queue: our thread queue
        :return: no return value.
        """
        name_list = self.determine_speaker()
        # name_list = self.determine_speaker_with_gender()
        self.speaker_threshold(name_list)
        ret_queue.put(name_list[0][0])

    def save_audio(self, frames, filename, audio):
        """
        function to save the microphone input for speaker recognition
        :param frames: the data frames of the input audio to be written to the file
        :param filename: name of file to save
        :param audio: our current pyAudio object
        :return: no return value.
        """
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(self.sample_format))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def get_command(self):
        """
        function to take in microphone input and determine what words the speaker said
        :return: the systems best guess of what the speaker said
        """
        # Set up the pyAudio stream for getting the user's speech from the microphone
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.sample_format,
                            channels=1,
                            rate=int(self.sample_rate),
                            input=True,
                            frames_per_buffer=self.frames_per_buffer)

        print("Listening for input: ")

        has_started_speaking = False
        sound_bites = []

        self.decoder.start_utt()
        while True:
            try:
                sound_bite = stream.read(self.frames_per_buffer)
            except IOError:
                raise
            else:
                sound_bites.append(sound_bite)

            if not sound_bite:
                # Do nothing
                continue

            # Process sound bite from microphone
            self.decoder.process_raw(sound_bite, False, False)
            is_speaking = self.decoder.get_in_speech()

            if is_speaking:
                has_started_speaking = True

            if not is_speaking and has_started_speaking:
                # User has stopped speaking, utterance is over
                self.decoder.end_utt()
                break

        hypothesis = self.decoder.hyp()
        best_guess = ''
        if hypothesis is not None:
            best_guess = hypothesis.hypstr

        print "I just heard you say: '{}'".format(best_guess)

        return best_guess
