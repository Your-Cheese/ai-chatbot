import sounddevice as sd
import flet as ft
import asyncio
import threading
import queue
import time

import twitchAPISetup
import LLM_API_requests
import TTS_Azure_API
import TTS_Coqui_Local
import transcription


async def main(page: ft.Page):
    # Start loops that run the separate threads
    loop = asyncio.get_running_loop()
    twitch_loop = asyncio.new_event_loop()
    LLM_loop = asyncio.new_event_loop()
    twitch_thread = threading.Thread(target=twitch_loop.run_forever, daemon=True).start()
    LLM_thread = threading.Thread(target=LLM_loop.run_forever, daemon=True).start()

    settings = dict()
    
    class settingsMenu():
        def __init__(self, name: str, options: list) -> None:
            self.name = name
            self.options = options
            self.changed = False
            self.menu = None
            self.dialog = None
            self.fields = [ft.Column(controls=[], tight=True)]
            self.row_count = 0
            self.column_count = 0
            
        async def build(self):
            for option, isPass in self.options:
                self.row_count += 1
                if self.row_count == 5:
                    self.row_count = 0
                    self.column_count += 1
                    self.fields.append(ft.Column(controls=[], tight=True))
                stored_option = await page.client_storage.get_async(option)
                if stored_option == None:
                    await page.client_storage.set_async(option, "")
                    stored_option = ""
                settings[option] = stored_option
                if isPass:
                    self.fields[self.column_count].controls.append(ft.TextField(label=option, value=settings[option], password=True, can_reveal_password=True))
                else:
                    self.fields[self.column_count].controls.append(ft.TextField(label=option, value=settings[option]))
            
            self.menu = ft.Row(self.fields, alignment=ft.MainAxisAlignment.CENTER)
            self.dialog = ft.AlertDialog(
                open=False,
                modal=False,
                title=ft.Text(self.name),
                content=ft.Container(content=self.menu, width=600*(self.column_count+1)),
                actions=[ft.ElevatedButton(text="Save", on_click=self.save_click), ft.ElevatedButton(text="Cancel", on_click=self.cancel_click)],
                actions_alignment="end",
            )

        def add_setting(self, control:ft.Control):
            self.row_count += 1
            if self.row_count == 5:
                self.row_count = 0
                self.column_count += 1
                self.fields.append(ft.Column(controls=[], tight=True))
            self.fields[self.column_count].controls.append(control)

        async def save_click(self, e):
            tasks = set()
            for column in self.menu.controls:
                for setting in column.controls:
                    settings[setting.label] = setting.value
                    # print(setting.label, setting.value, type(setting.value))
                    task = asyncio.create_task(page.client_storage.set_async(setting.label, setting.value))
                    tasks.add(task)
                    task.add_done_callback(tasks.discard)
            self.dialog.open = False
            self.changed = True
            await page.update_async()

        async def cancel_click(self, e):
            self.dialog.open = False
            await page.update_async()
    
    class errorMessage():
        def __init__(self, name:str, error:Exception) -> None:
            self.name = name
            self.error = error

        async def close_dialog(self, e):
            self.dialog.open = False
            await page.update_async()
        
        def build(self):
            self.dialog = ft.AlertDialog(
                open=True,
                modal=True,
                title=ft.Text(self.name),
                content=ft.Text(self.error),
                actions=[ft.ElevatedButton(text="OK", on_click=self.close_dialog)]
            )
            return self.dialog

    async def open_settings_click(e):
        page.dialog = setting_dialog.dialog
        setting_dialog.dialog.open=True
        await page.update_async()

    async def open_prompt_click(e):
        page.dialog = prompt_dialog.dialog
        prompt_dialog.dialog.open=True
        await page.update_async()

    async def Twitch_on():
        twitch_button.disabled = True
        asyncio.run_coroutine_threadsafe(page.update_async(), loop)
        if thisChat.twitch == None or setting_dialog.changed:
            thisChat.update(settings["Twitch App ID"], settings["Twitch App Secret"], settings["Twitch Target Channel"])
            result = asyncio.run_coroutine_threadsafe(thisChat.twitch_connect(), twitch_loop).result()
            setting_dialog.changed = False
        # print("Creating chat")
        result = asyncio.run_coroutine_threadsafe(thisChat.chat_connect(), twitch_loop).result()
        
        twitch_button.disabled = False
        twitch_button.content.controls[0].color = ft.colors.GREEN
        # AI_button.disabled=False

    async def toggle_Twitch_click(e):
        try:
            if thisChat.chat == None:
                await Twitch_on()
            elif thisChat.chat.is_connected():
                thisChat.chat.stop()
                twitch_button.content.controls[0].color = ft.colors.RED
                # if conversation_button.content.controls[0].color == ft.colors.RED:
                #     await stop_LLM()
                #     AI_button.disabled = True
            else:           
                await Twitch_on()
        except Exception as exc:
            twitch_error = errorMessage("Twitch Error", exc)
            page.dialog = twitch_error.build()
            twitch_button.disabled = False
            await page.update_async()

        await page.update_async()
    
    async def LLM_Requests():
        thisTTS = None
        AI_button.disabled = True
        # print("waiting for update")
        asyncio.run_coroutine_threadsafe(page.update_async(), loop)
        # print("update done")
        # print(isinstance(TTS_service.value, str))

        # Choose TTS Service to use
        if TTS_service.value == "0":
            thisTTS = TTS_Coqui_Local.Coqui_TTS()
        elif TTS_service.value == "1":
            # print("azure inputs:", settings["Azure Subscription Key"], settings["Azure Service Region"], settings["Azure TTS Voice"])
            try:
                thisTTS = TTS_Azure_API.Azure_TTS(settings["Azure Subscription Key"], settings["Azure Service Region"], settings["Azure TTS Voice"], settings["Azure TTS Voice Pitch"], settings["Azure TTS Voice Role"], settings["Azure TTS Voice Style"])
            except asyncio.exceptions.TimeoutError as exc:
                # print("error: ", exc)
                TTS_error = errorMessage("Azure TTS Timeout Error", "Check your Azure subscription") 
                page.dialog = TTS_error.build()
                # print("error done")
                AI_button.disabled = False
                asyncio.run_coroutine_threadsafe(page.update_async(), loop)
                return
        AI_button.disabled = False
        # flush_button.disabled=False
        AI_button.content.controls[0].color = ft.colors.GREEN
        asyncio.run_coroutine_threadsafe(page.update_async(), loop)

        # This is the main loop that gets the speech transcript and provides the output as a TTS every 5 seconds
        # Context is updated with the Twitch Chat
        # The loop is exited when it reads a message that says "STOP"
        
        current_time = time.perf_counter()
        user_name = settings["User Name"]
        prompt = settings["Prompt"]
        name = settings["Character Name"]
        context = "### Chat: \n"
        while(True):
            # print("getting message")
            priority, message = thisChat.chatMessages.get()
            if isinstance(message, str):
                if message == "STOP":
                    # print("Broke")
                    break
                # print(f"Got a message: {user_name} said: {message}")
                context += f"{user_name}: {message} \n"
            else:
                # print(f"Got a message: in {message.room.name}, {message.user.name} said: {message.text}")
                context += f"{message.user.name}: {message.text} \n"
            if len(prompt + context + "### " + name + ": ") > 2048:
                next_line = context.find("\n") + 2
                context = context[next_line:]
            # print(time.perf_counter() - current_time)
            if time.perf_counter() - current_time >= 5 or priority < 4:
                context += f"### {name} : "
                # print("getting LLM output")
                text_out = LLM_API_requests.getLLMOutput(prompt + context)
                # print("synthesizing speech with", audio_output_device.value, thisTTS)
                await thisTTS.speech_synthesis(text=text_out, audio_device=audio_output_device.value)
                # print("finished synthesis")
                context += f"{text_out} \n### Chat: "
                current_time = time.perf_counter()

    async def stop_LLM():
        LLM_loop.call_soon_threadsafe(thisChat.chatMessages.put((0, "STOP")))
        # flush_button.disabled=True
        AI_button.content.controls[0].color = ft.colors.RED
        await page.update_async()

    async def toggle_LLM_click(e):
        if AI_button.content.controls[0].color == ft.colors.RED:
            # print("Started LLM")
            asyncio.run_coroutine_threadsafe(LLM_Requests(), LLM_loop)
        else:
            await stop_LLM()

    def clear_queue(queue: queue.PriorityQueue):
        while not queue.empty():
            queue.get_nowait()
            queue.task_done()
        
    def flush_LLM_click(e):
        LLM_loop.call_soon_threadsafe(clear_queue(thisChat.chatMessages))
    
    
    async def toggle_conversation_mode(e):
        try:
            if conversation_button.content.controls[0].color == ft.colors.RED:
                conversation_button.disabled = True
                await page.update_async()
                # print(audio_input_device.value)
                tts.recognize_speech(audio_input_device=audio_input_device.value)
                conversation_button.disabled = False
                conversation_button.content.controls[0].color = ft.colors.GREEN
                # AI_button.disabled = False
            else:
                conversation_button.disabled = True
                # if twitch_button.content.controls[0].color == ft.colors.RED:
                #     await stop_LLM()
                #     AI_button.disabled = True
                await page.update_async()
                tts.stop_listening_for_audio()
                conversation_button.disabled = False
                conversation_button.content.controls[0].color = ft.colors.RED
        except Exception as exc:
            twitch_error = errorMessage("Whisper Error", exc)
            page.dialog = twitch_error.build()
            conversation_button.disabled = False
        await page.update_async()

    # Create each of the buttons to be used
    AI_button = ft.ElevatedButton(content=ft.Row([ft.Icon(name=ft.icons.POWER_SETTINGS_NEW, color=ft.colors.RED, size=30), ft.Text(value="AI", size=30)]), on_click=toggle_LLM_click)
    flush_button = ft.ElevatedButton(content=ft.Text(value="Flush", size=30), on_click=flush_LLM_click)
    conversation_button = ft.ElevatedButton(content=ft.Row([ft.Icon(name=ft.icons.POWER_SETTINGS_NEW, color=ft.colors.RED, size=30), ft.Text(value="Conversation Mode", size=30)]), on_click=toggle_conversation_mode)
    twitch_button = ft.ElevatedButton(content=ft.Row([ft.Icon(name=ft.icons.POWER_SETTINGS_NEW, color=ft.colors.RED, size=30), ft.Text(value="Twitch Connection", size=30)]), on_click=toggle_Twitch_click)

    col1 = ft.Column([AI_button, flush_button], alignment=ft.MainAxisAlignment.CENTER)
    col2 = ft.Column([conversation_button, twitch_button], alignment=ft.MainAxisAlignment.CENTER)


    setting_dialog = settingsMenu("Settings", [("Twitch App ID", True), ("Twitch App Secret", True), ("Twitch Target Channel", False), ("Azure Subscription Key", True), ("Azure Service Region", False), ("Azure TTS Voice", False), ("Azure TTS Voice Pitch", False), ("Azure TTS Voice Role", False), ("Azure TTS Voice Style", False)])
    prompt_dialog = settingsMenu("Prompt Settings", [("User Name", False), ("Character Name", False), ("Prompt", False)])
    # loading_dialog = ft.AlertDialog(content=ft.Stack([ft.ProgressRing()]), content_padding=ft.padding.only(left=125, top=20), modal=True, open=False)
    
    build_settings = asyncio.create_task(setting_dialog.build())
    build_prompt = asyncio.create_task(prompt_dialog.build())
    await build_settings
    await build_prompt

    audio_output_devices = []
    audio_input_devices = []

    in_device = await page.client_storage.get_async("Audio Input Device")
    out_device = await page.client_storage.get_async("Audio Output Device")

    if in_device != None:
        settings["Audio Input Device"] = int(in_device)   

    if out_device != None:
        settings["Audio Output Device"] = int(out_device)

    for idx, device in enumerate(sd.query_devices()):
        if device.get("max_output_channels") == 0:
            audio_input_devices.append(ft.dropdown.Option(key=idx, text=device.get("name")))
            if in_device == None:
                settings["Audio Input Device"] = idx
                await page.client_storage.set_async("Audio Input Device", idx)
        elif device.get("max_input_channels") == 0:
            audio_output_devices.append(ft.dropdown.Option(key=idx, text=device.get("name")))
            if out_device == None:
                settings["Audio Output Device"] = idx
                await page.client_storage.set_async("Audio Output Device", idx)

    audio_input_device = ft.Dropdown(label="Audio Input Device", options=audio_input_devices, value=settings["Audio Input Device"])
    setting_dialog.add_setting(audio_input_device)

    audio_output_device = ft.Dropdown(label="Audio Output Device", options=audio_output_devices, value=settings["Audio Output Device"])
    setting_dialog.add_setting(audio_output_device)


    TTS_service_value = await page.client_storage.get_async("TTS Service")
    if TTS_service_value == None:
        settings["TTS Service"] = 0
        await page.client_storage.set_async("TTS Service", 0)
    settings["TTS Service"] = TTS_service_value
    TTS_service = ft.Dropdown(label="TTS Service", options=[ft.dropdown.Option(key=0, text="Coqui TTS"), ft.dropdown.Option(key=1, text="Azure TTS")], value=settings["TTS Service"])
    setting_dialog.add_setting(TTS_service)

    thisChat = twitchAPISetup.twitchChatGetter(settings["Twitch App ID"], settings["Twitch App Secret"], settings["Twitch Target Channel"])
    tts = transcription.speech_to_text(thisChat.chatMessages)
    
    page.appbar = ft.AppBar(leading_width=40,
        title=ft.Text("AI Chatbot Dashboard"),
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.TEXTSMS_ROUNDED, on_click=open_prompt_click),
            ft.IconButton(ft.icons.SETTINGS_ROUNDED, on_click=open_settings_click)
        ]
    )
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.vertical_alignment=ft.MainAxisAlignment.SPACE_AROUND
    await page.add_async(ft.Row([col1, col2], alignment=ft.MainAxisAlignment.SPACE_AROUND))

if __name__ == '__main__':
    ft.app(target=main)