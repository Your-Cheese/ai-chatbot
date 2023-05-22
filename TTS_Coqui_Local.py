from TTS.api import TTS
import sounddevice as sd
import numpy as np
import asyncio

class Coqui_TTS():
    def __init__(self, model:str="tts_models/en/vctk/vits", speaker:str=1) -> None:
        
        # print("Creating Coqui TTS")
        self.model_name = model
        # print("made model")
        self.tts = TTS(self.model_name)
        self.speaker = speaker
        self.generated = None
        self.idx = 0
        self.loop = asyncio.get_event_loop()
        self.event = asyncio.Event()
        # print("making audio stream")
        self.stream = None
        
        

    async def speech_synthesis(self, text:str, audio_device:int):
        # print("generating audio")
        if self.stream != None:
            await self.event.wait()
            self.stream.close()
            self.event.clear()
            self.idx = 0

        self.generated = np.transpose(np.reshape(np.array(self.tts.tts(text=text, speaker=self.tts.speakers[self.speaker]), dtype=np.float32), (1, -1)))
        # WIDTH = 2
        # CHANNELS = 1
        # RATE = 22050
        
        # print(self.generated.dtype.name)
        self.stream = sd.OutputStream(
            channels=self.generated.shape[1],
            samplerate=22050,
            dtype=self.generated.dtype,
            device=audio_device,
            callback=self.callback
        )

        # print("done generating")
        self.stream.start()

    def callback(self, outdata, frames, time, status):
        if status:
            print(status)
        remainder = len(self.generated) - self.idx
        if remainder == 0:
            self.loop.call_soon_threadsafe(self.event.set)
            raise sd.CallbackStop
        valid_frames = frames if remainder >= frames else remainder
        outdata[:valid_frames] = self.generated[self.idx:self.idx + valid_frames]
        outdata[valid_frames:] = 0
        self.idx += valid_frames
