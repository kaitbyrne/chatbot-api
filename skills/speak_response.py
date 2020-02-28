import pyttsx

def speak_response(resp_input):
    engine = pyttsx.init()
    engine.say(resp_input)
    engine.runAndWait()
