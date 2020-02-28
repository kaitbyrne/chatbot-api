import os
import time
import wave
import pyaudio
import subprocess

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 8192
RECORD_SECONDS = 10


def speak_response(resp_input):
    """
    Simple function to speak a skill result
    :param resp_input: speaks this result
    """
    print(resp_input)
    subprocess.call('say ' + resp_input, shell=True)


def setup_func(name):
    """
    Function to record and store user audio for training on our recognition model
    :param name: the name of the speaker we are training on
    :return: no return value.
    """
    audio = pyaudio.PyAudio()

    print("When you see 'recording...' record speech until it says it has "
          "completed\n12 speech samples will be recorded\n\n")

    if not os.path.exists("./train_data/%s" % (name.lower())):
        os.makedirs("./train_data/%s" % (name.lower()))

    for i in range(0, 11):
        cmd = "recording. start now."
        if i == 11:
            cmd = "final recording. start now."
        speak_response(cmd)
        wave_output_filename = ("./train_data/%s/%s%d.wav" % (name.lower(), name.lower(), i))

        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

        print("\nrecording...\n")
        frames = []

        for x in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        cmd = "recording complete. please wait for the next one."
        if i == 11:
            cmd = "final recording complete. thank you."
        speak_response(cmd)
        print("%s complete" % wave_output_filename)

        stream.stop_stream()
        stream.close()

        wave_file = wave.open(wave_output_filename, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()

        time.sleep(3)


if __name__ == "__main__":
    setup_func('test')
