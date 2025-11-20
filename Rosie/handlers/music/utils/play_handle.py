import asyncio
from telethon import Button
from core.replies import font_style
from pytgcalls.types import MediaStream






current_song = {}
queue_songs = {}



def make_seekbar(current_sec: int, total_sec: int, bar_length: int = 12):
    # Convert seconds → mm:ss
    def fmt(t):
        m = t // 60
        s = t % 60
        return f"{m:02d}:{s:02d}"

    # Safety
    if total_sec == 0:
        total_sec = 1

    # Progress index
    filled = int((current_sec / total_sec) * bar_length)

    bar = "━" * filled + "●" + "━" * (bar_length - filled)

    return f"{fmt(current_sec)}  {bar}  {fmt(total_sec)}"


def display_time(sec_str: int):
    # string → int convert
    total = int(sec_str)

    hours = total // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60

    # अगर hours नहीं हैं तो सिर्फ MM:SS
    if hours == 0:
        return f"{minutes:02d}:{seconds:02d}"
    else:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"



async def play_song(event, vc, song, force=False):
    chat_id = event.chat_id

    # If already playing something & force=False → add to queue
    if chat_id in current_song and not force:
        await add_to_queue(event, song)
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
    await event.respond(
        final_msg,
        file=thumb,
        buttons=music_buttons,
        parse_mode="html",
        link_preview=False,
    )
        






async def add_to_queue(event, song):
    
    chat_id = event.chat_id 
    
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
    
    await event.respond(final_msg, buttons=music_buttons, parse_mode="html", link_preview=False) 
        
     


async def play_next_song(event, vc):
    chat_id = event.chat_id
    
    if chat_id not in current_song:
        raise Exception("bot not streaming")
    
    if chat_id not in queue_songs:
        queue_songs[chat_id] = []
    
    chat_queue = queue_songs[chat_id] 
    
    try:
        next_song = chat_queue.pop(0)
    except:
        current_song.pop(chat_id)  
        return False  
    
    asyncio.create_task(play_song(event, vc, next_song, force=True))
    return True   