import azure.cognitiveservices.speech as speechsdk
import sounddevice as sd
import asyncio
import sys

class Azure_TTS():
    def __init__(self, subscription_key:str, region:str, voice:str, pitch:str, role:str, style:str) -> None:
        # print("Creating a speech synthesizer...")

        speech_key = subscription_key
        service_region = region
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Raw24Khz16BitMonoPcm)
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        self.voice = voice
        self.pitch = pitch
        self.role = role
        self.style = style
        self.loop = asyncio.get_event_loop()
        self.event = asyncio.Event()
        self.sdstream = None

    async def speech_synthesis(self, text:str, audio_device:int):
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        ssml_string = """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
            <voice name="{}">
                <prosody pitch="{}">
                    <mstts:express-as role="{}" style="{}">
                    {}
                    </mstts:express-as>
                </prosody>
            </voice>
        </speak>""".format(self.voice, self.pitch, self.role, self.style, text)
        if self.sdstream != None:
            await self.event.wait()
            self.sdstream.close()
            self.event.clear()
        # print("getting speech")
        result = self.speech_synthesizer.speak_ssml_async(ssml_string).get()
        self.stream = speechsdk.AudioDataStream(result)
        # print("stream done")
        # filesaved = self.stream.save_to_wav_file("test1.wav")
        # print("saved to file")
        
        self.sdstream = sd.RawOutputStream(
            samplerate=24000, 
            device=audio_device, channels=1, dtype='int16',
            callback=self.callback)
        
        # print("starting stream")
        self.sdstream.start()

    def callback(self, outdata, frames, time, status):
        if status.output_underflow:
            print('Output underflow: increase blocksize?', file=sys.stderr)
            raise sd.CallbackAbort
        assert not status
        data = bytes(len(outdata))
        buffer_size = self.stream.read_data(data)
        if buffer_size == 0:
            self.loop.call_soon_threadsafe(self.event.set)
            raise sd.CallbackStop
        # print(buffer_size, len(outdata))
        # assert buffer_size == len(outdata)
        outdata[:] = data