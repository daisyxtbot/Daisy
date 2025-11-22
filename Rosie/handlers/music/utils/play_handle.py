import asyncio
from telethon import Button
from core.replies import font_style
from pytgcalls.types import MediaStream






current_song = {}
queue_songs = {}



def make_seekbar(current_sec: int, total_sec: int, bar_length: int = 12):
    # Convert seconds → mm:ss or hh:mm:ss
    def fmt(t):
        h = t // 3600
        m = (t % 3600) // 60
        s = t % 60

        if h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}"   # HH:MM:SS
        else:
            return f"{m:02d}:{s:02d}"           # MM:SS

    # Safety
    if total_sec <= 0:
        total_sec = 1

    # Progress index
    filled = int((current_sec / total_sec) * bar_length)
    if filled > bar_length:
        filled = bar_length

    bar = "━" * filled + "●" + "━" * (bar_length - filled)

    return f"{fmt(current_sec)}  {bar}  {fmt(total_sec)}"


def display_time(sec_str: int):
    # string → int convert
    total = int(sec_str)

    hours = total // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60

    
    if hours == 0:
        return f"{minutes:02d}:{seconds:02d}"
    else:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


async def update_seekbar(msg, vc, song):
    chat_id = msg.chat_id
    msg_id = msg.id
    total = int(song["duration"])

    # Loop forever until message changes or song changes
    while True:

        #  Song changed in this chat STOP
        if chat_id not in current_song:
            return
        
        #  A new message ID has replaced this STOP
        if current_song[chat_id].get("msg_id") != msg_id:
            return

        # Try getting current stream position
        try:
            res = await vc.time(chat_id)
        except:
            return
        
        # Build seekbar
        new_seekbar = make_seekbar(int(res), total)

        music_buttons = [
            [
                Button.inline("«", b"music_seekback"),
                Button.inline("▢", b"music_stop"),
                Button.inline("।।", b"music_pause"),
                Button.inline("»", b"music_seekforward"),
            ],
            [Button.inline(new_seekbar, b"music_seekbar")],
            [Button.inline("⌞ ᴄʟᴏsᴇ ⌝", b"music_close")],
        ]

        # Update UI
        try:
            await msg.edit(buttons=music_buttons)
        except:
            pass

        await asyncio.sleep(1)
    
    


async def play_song(client, vc, song, force=False):
    chat_id = song["req_by"]["chat_id"]

    # If already playing something & force=False → add to queue
    if chat_id in current_song and not force:
        await add_to_queue(client, song)
        return

    # Set current song
    current_song[chat_id] = song

    # Song info
    req_by = song.get("req_by", {})
    first_name = req_by.get("first_name", "Unknown")
    username = req_by.get("username")

    # Mention build
    if username:
        mention = f'<a href="https://t.me/{username}">{first_name}</a>'
    else:
        mention = first_name

    song_name = song.get("title", "Unknown Song")
    title = font_style.to_smallcaps(song_name[:21])

    song_url = song.get("url", "#")
    song_time = int(song.get("duration", 0))
    time = display_time(song_time)

    thumb = song.get("thumbnail")
    stream_link = song.get("stream_url")
    mode = song.get("mode", "song")
    # Header
    header_msg = "<b>ɴᴏᴡ ᴘʟᴀʏɪɴɢ</b>"
    header_mention = f'<a href="{song_url}">{header_msg}</a>'

    playback_msg = (
        f"➟ ᴛɪᴛʟᴇ : {title}\n"
        f"➟ ᴅᴜʀᴀᴛɪᴏɴ : {time}\n"
        f"➟ ʀᴇǫ ʙʏ : {mention}"
    )

    final_msg = f"<blockquote>{header_mention}</blockquote>\n{playback_msg}"

    # Seekbar
    seekbar = make_seekbar(0, song_time)

    # UI BUTTONS
    music_buttons = [
        [
            Button.inline("«", b"music_seekback"),
            Button.inline("▢", b"music_stop"),
            Button.inline("।।", b"music_pause"),
            Button.inline("»", b"music_seekforward"),
        ],
        [Button.inline(seekbar, b"music_seekbar_dummy")],
        [Button.inline("⌞ ᴄʟᴏsᴇ ⌝", b"music_close")],
    ]
    
    # play using pytgcalls as vc
    
    video_flag = None
    if mode == "song":
        video_flag = MediaStream.Flags.IGNORE
        
    try:
        await vc.play(
            chat_id,
            MediaStream(
                stream_link,
                video_flags=video_flag,
            ),
        )
    except Exception as e:
        current_song.pop(chat_id, None)
        if "Chat admin privileges are required" in str(e):
            await event.reply(event.get_reply("vc_not_opened"))
            return
        else:
            raise e    
        
        
    # Send message
    msg = await client.send_file(
        chat_id,
        file=thumb,
        caption=final_msg,
        buttons=music_buttons,
        parse_mode="html",
        link_preview=False,
    )
    
    current_song[chat_id]["msg_id"] = msg.id
    
    asyncio.create_task(update_seekbar(msg, vc, song))
    
        






async def add_to_queue(client, song):
    
    chat_id = song["req_by"]["chat_id"]
    
    if not chat_id in queue_songs:
        queue_songs[chat_id] = []
        
    
    chat_queue = queue_songs[chat_id]
    chat_queue.append(song)
    
    song_count = len(chat_queue)
    
    req_by = song["req_by"]
    first_name = req_by["first_name"]
    username = req_by["username"]
    
    mention = f'<a href="https://t.me/{username}">{first_name}</a>'
    if not username:
        mention = first_name
    
    song_name = song["title"]
    title = font_style.to_smallcaps(song_name[:21])
    song_url = song["url"]  
    song_time = int(song["duration"])
    time = display_time(song_time)
    thumb = song["thumbnail"]
        
    header_msg = f"<b>ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ #{song_count}</b>" 
    header_mention = f'<a href="{song_url}">{header_msg}</a>'
    
    playback_msg = f"""➟ ᴛɪᴛʟᴇ : {title}
➟ ᴅᴜʀᴀᴛɪᴏɴ : {time}
➟ ʀᴇǫ ʙʏ : {mention}"""
    
    final_msg = f"<blockquote>{header_mention}</blockquote>\n{playback_msg}"  
    
   
    music_buttons = [
        [Button.inline(f"⌞ ᴄʟᴏsᴇ ⌝", b"music_close")]
    ]
    
    await client.send_message(chat_id, final_msg, buttons=music_buttons, parse_mode="html", link_preview=False) 
        
     


async def play_next_song(client, chat_id, vc):
    
    if chat_id not in current_song:
        raise Exception("bot not streaming")
    
    if chat_id not in queue_songs:
        queue_songs[chat_id] = []
    
    chat_queue = queue_songs[chat_id] 
    
    try:
        next_song = chat_queue.pop(0)
    except:
        current_song.pop(chat_id) 
        await vc.leave_call(
            chat_id,
            ) 
        return False  
    
    asyncio.create_task(play_song(client, vc, next_song, force=True))
    return True  



async def end_song(client, chat_id, vc):
    
    if chat_id not in current_song:
        raise Exception("bot not streaming")
    
    try:
        current_song.pop(chat_id) 
        await vc.leave_call(
            chat_id,
            ) 
    except:
        raise Exception("bot not streaming")
         
    
     