import traceback
import sys
import subprocess
from Queue import Queue
import pocket_sphinx_listener as psl
from skills.hello import hello_helper
from skills.news import news_helper
from skills.weather import weather_helper
from skills.date_time import *
from skills.goodbye import goodbye_helper
from skills.github_connect import github_helper
from skills.fun_facts import fun_facts_helper
from skills.jokes import jokes_helper
from model.train_classifier import find_skill
from model.model_enum import Model
from model.chatbot import chat_helper


def speak_response(resp_input):
    """
    Simple function to speak a skill result
    :param resp_input: speaks this result
    """
    print(resp_input)
    subprocess.call('say ' + resp_input, shell=True)


def base_skill_finder(found_skill, user_input):
    """
    Simple function to speak a skill result
    :param resp_input: speaks this result
    """
    if found_skill == 'hello':
        return  hello_helper()
    elif found_skill == 'news':
        return  news_helper()
    elif found_skill == 'weather':
        return  weather_helper()
    elif found_skill == 'date':
        return date_helper()
    elif found_skill == 'time':
        return time_helper()
    elif found_skill == 'github_connect':
        return github_helper(user_input)
    elif found_skill == 'fun_facts':
        return fun_facts_helper()
    elif found_skill == 'jokes':
        return jokes_helper()
    elif found_skill == 'goodbye':
        return goodbye_helper()


def main():
    """
    Main loop for speaking commands into bot
    Pocketsphinx listener used to convert speech to text
    Responds spoken function returns until bot is quit
    """
    # Set an initial condition.
    chatbot_active = True
    speak_response("How can I help you today?")

    # Set up the voice recognition using Pocketsphinx from CMU Sphinx.
    keyword_listener = psl.PocketSphinxListener(model=Model.KEYWORD.value)
    pocket_sphinx_listener = psl.PocketSphinxListener(model=Model.STANDARD.value)

    # Run until goodbye command or SIGINT (ctrl+c)
    while chatbot_active:
        try:
            user_input_keyword = keyword_listener.get_command().lower()

            if 'hey ron' in user_input_keyword:
                try:
                    user_input = pocket_sphinx_listener.get_command().lower()
                    speakers = Queue()
                    pocket_sphinx_listener.check_speaker_recognition(speakers)
                    speaker = speakers.get()
                    found_skill = find_skill(user_input)

                    if found_skill == 'chat':
                        speak_response('What do you want to talk about?')
                        chat_input = pocket_sphinx_listener.get_command().lower()
                        chat_out = chat_helper(chat_input)
                        speak_response(chat_out)
                    elif found_skill == 'goodbye':
                        response = base_skill_finder('goodbye')
                        speak_response(response)
                        chatbot_active = False
                    else:
                        response = base_skill_finder(found_skill)
                        speak_response(response)

                except (KeyboardInterrupt, SystemExit):
                    speak_response('Goodbye')
                    chatbot_active = False
                    sys.exit(0)

        except (KeyboardInterrupt, SystemExit):
            speak_response('Goodbye')
            chatbot_active = False
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
            sys.exit(1)


if __name__ == '__main__':
    main()
