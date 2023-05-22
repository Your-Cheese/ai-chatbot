from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
import queue

class twitchChatGetter():

    def __init__(self, APP_ID: str, APP_SECRET: str, TARGET_CHANNEL: str):
        self.APP_ID = APP_ID
        self.APP_SECRET = APP_SECRET
        self.TARGET_CHANNEL = TARGET_CHANNEL
        self.USER_SCOPE = [AuthScope.CHAT_READ]
        self.twitch = None
        self.chat = None
        self.chatMessages = queue.PriorityQueue()

    def update(self, APP_ID: str, APP_SECRET: str, TARGET_CHANNEL: str):
        self.APP_ID = APP_ID
        self.APP_SECRET = APP_SECRET
        self.TARGET_CHANNEL = TARGET_CHANNEL
    
    async def twitch_connect(self):
        # print("Setting up Twitch with", self.APP_ID, self.APP_SECRET)
        self.twitch = Twitch(self.APP_ID, self.APP_SECRET)
        # print("Got Twitch")
        auth = UserAuthenticator(self.twitch, self.USER_SCOPE)
        # print("Authenticated")
        try:
            # print("auth started")
            token, refresh_token = await auth.authenticate()
            # print("got token")
            await self.twitch.set_user_authentication(token, self.USER_SCOPE, refresh_token)
            # print("complete")
        except:
            print("Authentication failed")
        # print("Twitch connected")

    # this will be called when the event READY is triggered, which will be on bot start
    async def on_ready(self, ready_event: EventData):
        # print('Bot is ready for work, joining channels')
        # join our target channel, if you want to join multiple, either call join for each individually
        # or even better pass a list of channels as the argument
        await ready_event.chat.join_room(self.TARGET_CHANNEL)
        # print("Joined", self.TARGET_CHANNEL)


    # this will be called whenever a message in a channel was send by either the bot OR another user
    async def on_message(self, msg: ChatMessage):
        self.chatMessages.put((4, msg))
        # print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')


    # this will be called whenever someone subscribes to a channel
    # async def on_sub(self, sub: ChatSub):
        # print(f'New subscription in {sub.room.name}:\\n'
        #     f'  Type: {sub.sub_plan}\\n'
        #     f'  Message: {sub.sub_message}')

    # this is where we set up the bot
    async def chat_connect(self):
        # create chat instance
        if self.chat == None:
            self.chat = await Chat(self.twitch)

            # register the handlers for the events you want

            # listen to when the bot is done starting up and ready to join channels
            self.chat.register_event(ChatEvent.READY, self.on_ready)
            # listen to chat messages
            self.chat.register_event(ChatEvent.MESSAGE, self.on_message)
            # listen to channel subscriptions
            # self.chat.register_event(ChatEvent.SUB, self.on_sub)
        # there are more events, you can view them all in this documentation

        # we are done with our setup, lets start this bot up!
        self.chat.start()
        # print("Bot started")

