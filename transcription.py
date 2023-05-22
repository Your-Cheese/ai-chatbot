import queue
import speech_recognition as sr


# this is called from the background thread

class speech_to_text():
    def __init__(self, chat:queue.PriorityQueue) -> None:
        self.r = sr.Recognizer()
        self.m = None
        self.chat = chat
        self.stop_listening = None
        
    def transcription_callback(self, recognizer:sr.Recognizer, audio:sr.AudioData):
        # received audio data, now we'll recognize it using Whisper
            try:
                text = recognizer.recognize_whisper(audio)
                # print("Whisper thinks you said " + text)
                self.chat.put((3, text))
            except sr.UnknownValueError:
                print("Whisper could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Whisper; {0}".format(e))

    def recognize_speech(self, audio_input_device:int):
        self.m = sr.Microphone(device_index=audio_input_device)
        # print("Microphone set up")
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stop_listening = self.r.listen_in_background(self.m, self.transcription_callback)
        # calling this function requests that the background listener stop listening

    def  stop_listening_for_audio(self):
        if self.stop_listening is not None:
            self.stop_listening(wait_for_stop=False)  # `wait_for_stop` set to `False` to terminate immediately