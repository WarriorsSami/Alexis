import datetime

import speech_recognition as sr


class AudioEngine(object):
    def __init__(self, engine):
        self.engine = engine
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        self.speech_unrecognizable = False

        self.record = False
        self.logs = open('Logging.txt', 'a+')
        self.logs.write('\n\n')
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.logs.write(str_time + '\n')

    def record_audio(self):
        self.speech_unrecognizable = False
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
            voice_data_local = ''
            try:
                voice_data_local = self.r.recognize_google(audio)
                if self.record is True:
                    self.logs.write('\nSami: ' + voice_data_local)
            except sr.UnknownValueError:
                self.bot_speak('Sorry, I did not get that')
                self.speech_unrecognizable = True
            except sr.RequestError:
                self.bot_speak('Sorry, my speech service is not working. I will stop my execution thread')
                exit()
            print('\nMe: ' + voice_data_local)
            return voice_data_local.lower()

    def record_main(self):
        while True:
            message = self.record_audio()
            if self.speech_unrecognizable is False:
                break
        return message

    def bot_speak(self, text):
        print('\nAlexis: ')
        self.engine.say(text)
        print(text)
        if self.record is True:
            self.logs.write('\nAlexis: ' + text)
        self.engine.runAndWait()
