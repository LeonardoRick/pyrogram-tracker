import asyncio
import sys
from iqlogger import Logger
from pathlib import Path
from pyrogram import Client as Telegram
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message, User
from pyrogram.errors import RPCError
from tlg_constants import TelegramConstants

# redirect log info to a file called log.txt (you should create this file)
sys.stdout = Logger(Path(__file__).parent.absolute())

tlgSessionPath = Path.joinpath(Path(__file__).parent.absolute(), 'tlgdb')
c = TelegramConstants()


tlg = Telegram(
    workdir=str(tlgSessionPath),
    session_name="leo123",  # change this last name to your session variable
    phone_number=c.phone,
    api_id=c.api_id,
    api_hash=c.api_hash,
)

async def main():
    i = 0
    while True:
        i += 1
        await asyncio.sleep(1)

# todo: try to make this work. After x = True I was supposed to be settled up but this is not happening
def my_start(attempt=0) -> User:
    try:
        x = tlg.connect()
        print(x)
        if not x:
            print('false')
    except RPCError as e:
        if attempt == 1:
            raise e
        my_start(1)
        raise e

# @tlg.on_message() # add this if you don't need to remove handler. Then, you should remove add_handler too
async def my_handler(client, update: Message):
    is_channel = update.chat.type == 'supergroup' or update.chat.type == 'channel'
    reply_to_message_id = update.reply_to_message.message_id if update.reply_to_message else None
    print(f'chat id: {update.chat.id}')
    print(f'id: {update.message_id}')
    print(f'msg: {update.text}')
    print(f'is_channel: {is_channel}')
    print(f'reply_to_message_id: {reply_to_message_id}')
    print('-----------------')

# @tlg.on_deleted_messages()
async def onDelete(client, update):
    print('DELETED')
    deleted_ids = []
    chat_id = update[0].chat.id if update[0].chat else None
    for message in update:
        deleted_ids.append(message.message_id)
    print('deleted ids:')
    print(deleted_ids)
    print(f'chat_id: {chat_id}')
    print(f'is_channel: {chat_id is not None}')
    print('-----------------')


try:
    print(f'listening to number: {c.phone}')
    handler = tlg.add_handler(MessageHandler(my_handler))
    tlg.start()
    # my_start()
    asyncio.get_event_loop().run_until_complete(main())
except KeyboardInterrupt:
    tlg.remove_handler(*handler)
    print('\nEvent removed and program finished.')
