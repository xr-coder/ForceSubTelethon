import logging
from telethon import TelegramClient, events, Button
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

API_ID = int("") #Fill Your Api Id
API_HASH = "" #Fill Your Api Hash
BOT_TOKEN = "" #Fill Your Bot token
GROUP_ID=int("") #Fill In Your Group ID
CHANNEL_ID = int("") #Fill In Your Channel Id
CHANNEL_USERNAME = "" #Fill Channel Username Without @ Sign

print("Force Sub Bot Is Starting...")

try:
    fsub = TelegramClient('fsub', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
except Exception as e:
    print(f"ERROR :- {str(e)}")
    exit()

async def get_user_join(id):
    id=await fsub.get_entity(id)
    st = True
    try:
        await fsub(GetParticipantRequest(channel=CHANNEL_USERNAME, participant=id))
        st = True
    except UserNotParticipantError:
        st =  False
    return st

@fsub.on(events.NewMessage(incoming=True))
async def mute_on_msg(event):
    if event.chat_id != GROUP_ID:
        return
    x = await get_user_join(event.sender_id)
    if x is False:
        try:
            await fsub.edit_permissions(GROUP_ID, event.sender_id, until_date=None, send_messages=False)
        except Exception as e:
            return
        await event.reply(f"**Hᴇʏ [{event.sender.first_name}](tg://user?id={event.sender_id}), Sᴇᴇᴍs Lɪᴋᴇ Yᴏᴜ Hᴀᴠᴇɴ'ᴛ Jᴏɪɴᴇᴅ Oᴜʀ Cʜᴀɴɴᴇʟ.**\n\n**Pʟᴇᴀsᴇ Jᴏɪɴ @{CHANNEL_USERNAME} Aɴᴅ Tʜᴇɴ Pʀᴇss Tʜᴇ Bᴜᴛᴛᴏɴ Bᴇʟᴏᴡ Tᴏ Uɴᴍᴜᴛᴇ Yᴏᴜʀsᴇʟғ!**", buttons=[[Button.url("Cʜᴀɴɴᴇʟ", url=f"https://t.me/{CHANNEL_USERNAME}")], [Button.inline("Uɴᴍᴜᴛᴇ Mᴇ", data=f"unmute_{event.sender_id}")]])


@fsub.on(events.callbackquery.CallbackQuery())
async def _(event):
    uid = event.data.decode("UTF-8").split("_")
    dat , uid = uid
    if dat != "unmute":
        return
    uid = int(uid)
    if uid == event.sender_id:
        x = await get_user_join(uid)
        if not x:
            await event.answer(f"Yᴏᴜ Hᴀᴠᴇ'ɴᴛ Jᴏɪɴᴇᴅ Tʜᴇ Cʜᴀɴɴᴇʟ Yᴇᴛ.\nFɪʀsᴛ Jᴏɪɴ Tʜᴇɴ Cʟɪᴄᴋ Tʜɪs Bᴜᴛᴛᴏɴ Aɢᴀɪɴ", cache_time=0, alert=True)
        else:
            try:
                await fsub.edit_permissions(GROUP_ID, uid, until_date=None, send_messages=True)
            except Exception as e:
                print(str(e))
                return
            await event.answer("Tʜᴀɴᴋs Fᴏʀ Jᴏɪɴɪɴɢ Nᴏᴡ ʏᴏᴜ Cᴀɴ Cʜᴀᴛ Hᴇʀᴇ" , alert=True)
            msg = f"**Wᴇʟᴄᴏᴍᴇ Tᴏ {(await event.get_chat()).title}, {event.sender.first_name} !**\n**Gᴏᴏᴅ Tᴏ Sᴇᴇ Yᴏᴜ Hᴇʀᴇ! As Yᴏᴜ Hᴀᴠᴇ Jᴏɪɴᴇᴅ Oᴜʀ Cʜᴀɴɴᴇʟ Nᴏᴡ Yᴏᴜ Cᴀɴ Cʜᴀᴛ Hᴇʀᴇ**"
            butt = [Button.url("Cʜᴀɴɴᴇʟ", url=f"https://t.me/{CHANNEL_USERNAME}")]
            await event.edit(msg, buttons=butt)
    else:
        await event.answer("Yᴏᴜ Aʀᴇ Aɴ Oʟᴅ Mᴇᴍʙᴇʀ Aɴᴅ Cᴀɴ Sᴘᴇᴀᴋ Fʀᴇᴇʟʏ! Tʜɪs Isɴ'ᴛ Fᴏʀ Yᴏᴜ!", cache_time=0, alert=True)

@fsub.on(events.NewMessage(pattern="/start"))
async def strt(event):
    await event.reply(f"**Hɪ, I'ᴍ A Fᴏʀᴄᴇ Sᴜʙsᴄʀɪʙᴇ Bᴏᴛ Sᴘᴇᴄɪᴀʟʟʏ Cᴏᴅᴇᴅ Bʏ @Legends_Nvr_Die Fᴏʀ @{CHANNEL_USERNAME}.**\n\n**Iғ Yᴏᴜ Wᴀɴᴛ Rᴇᴘᴏ Oғ Tʜɪs Bᴏᴛ Pʟᴇᴀsᴇ Cᴏɴᴛᴀᴄᴛ @Legends_Nvr_Die**", buttons=[Button.url("Cʜᴀɴɴᴇʟ", url=f"https://t.me/{CHANNEL_USERNAME}")])

    
print("ForceSub Bot has started.\nDo /start In Bot PM")
fsub.run_until_disconnected()
