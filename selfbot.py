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

clients = []

class MyClient(discord.Client):
    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token

    async def on_ready(self):
        print(f'Logged in as {self.user} ({self.user.id})')
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f'{self.user} is online!')

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
