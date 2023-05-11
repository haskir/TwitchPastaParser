import os

import dotenv
from twitchio.ext import commands, routines
from Functions import skip


class Bot(commands.Bot):
    def __init__(self, access_token: str, streamers: list):
        path = "./messages.txt"
        self.message_file = open(path, "a")
        self.error_file = open("./errors.txt", "a", encoding="utf-8")
        super().__init__(token=access_token, prefix='?', initial_channels=streamers)

    async def streamers(self, maximum: int = 30) -> list[str]:
        streamers = await self.fetch_streams(game_ids=[29595],
                                             languages=["ru"],
                                             type="live")
        streamers = [streamer.user.name for streamer in
                     sorted(streamers, reverse=True, key=lambda streamer: streamer.viewer_count)]
        return streamers[:maximum:]

    @routines.routine(minutes=30)
    async def connect_to_current_streamers(self):
        new_channels = await self.streamers()
        current_channels = [channel.name for channel in self.connected_channels]
        print(f"{current_channels = }")
        channels_to_leave = [channel for channel in current_channels
                             if channel not in new_channels]
        await self.part_channels(channels_to_leave)
        channels_to_join = [channel for channel in new_channels
                            if channel not in current_channels]
        await self.join_channels(channels_to_join)
        print(await self.streamers())

    async def event_message(self, message):
        if not skip(message):
            print(f"{message.channel.name} ->  {message.author.name}: {message.content}")
            try:
                self.message_file.write(f"{message.content}\n")
            except UnicodeEncodeError:
                self.error_file.write(f"{message.content}\n")

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        self.connect_to_current_streamers.start()


if __name__ == "__main__":
    dotenv.load_dotenv()
    ACCESS_TOKEN: str = os.getenv("ACCESS_TOKEN")
    REFRESH_TOKEN: str = os.getenv("REFRESH_TOKEN")
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    current: list = ["lapkinastol"]
    bot = Bot(ACCESS_TOKEN, current)
    bot.run()
