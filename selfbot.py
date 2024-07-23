import discord
import asyncio
from dotenv import load_dotenv
import os
from keep_alive import keep_alive  # Import the keep_alive function

# Load environment variables from .env file
load_dotenv()

# Get tokens and channel ID from environment variables
TOKENS = [os.getenv('TOKEN_1'), os.getenv('TOKEN_2'), os.getenv('TOKEN_3')]
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
AUTHORIZED_USER_ID = 387923086730723329  # Replace with your user ID

# Define the intents
intents = discord.Intents.default()
intents.messages = True  # Ensure the bot can receive message events
intents.message_content = True  # Enable message content intent for reading messages
intents.voice_states = True  # Enable voice state intent to manage voice channels

clients = []

class MyClient(discord.Client):
    def __init__(self, token, *args, **kwargs):
        super().__init__(intents=intents, *args, **kwargs)  # Pass intents to the superclass constructor
        self.token = token

    async def on_ready(self):
        print(f'Logged in as {self.user} ({self.user.id})')
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f'{self.user} is online!')

    async def on_message(self, message):
        if message.author.id != AUTHORIZED_USER_ID:
            return  # Ignore messages from unauthorized users
        
        if message.content.startswith('?join'):
            try:
                channel_id = int(message.content.split(' ')[1])
                channel = self.get_channel(channel_id)
                if isinstance(channel, discord.VoiceChannel):
                    for client in clients:
                        await client.join_voice_channel(channel)
            except Exception as e:
                print(f'Error: {e}')

    async def join_voice_channel(self, channel):
        if self.voice_clients:
            await self.voice_clients[0].disconnect()
        await channel.connect()

    async def start_bot(self):
        await self.start(self.token)

async def main():
    keep_alive()  # Call the keep_alive function
    for token in TOKENS:
        client = MyClient(token)
        clients.append(client)
        asyncio.create_task(client.start_bot())

    await asyncio.gather(*[client.wait_until_ready() for client in clients])

asyncio.run(main())
