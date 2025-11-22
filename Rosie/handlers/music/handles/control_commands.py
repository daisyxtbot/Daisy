import asyncio
from ..utils.play_handle import play_next_song, end_song





async def handle(event, vc):
    
    command = event.command
    
    if command == "skip":
        await skip_handle(event, vc)
    elif command == "end":
        await end_handle(event, vc)

    
async def end_handle(event, vc):
    
    try:
        await end_song(event.client, event.chat_id, vc)
    except Exception as e:
        if "bot not streaming" in str(e):
            await event.reply(event.get_reply("bot_not_streaming"))
        else:
            await event.reply(f"{e}")
        return 
    
    try:
        await event.delete()
    except:
        pass    
    
    sent = await event.reply(event.get_reply("ended"))
    
    await asyncio.sleep(2)
    await sent.delete()    
        
          
    

async def skip_handle(event, vc):
    try:
        await play_next_song(event.client, event.chat_id, vc)
    except Exception as e:
        if "bot not streaming" in str(e):
            await event.reply(event.get_reply("bot_not_streaming"))
        else:
            await event.reply(f"{e}")
        return    
    
    try:
        await event.delete()
    except:
        pass 
        
    sent = await event.reply(event.get_reply("skipped"))
    
    await asyncio.sleep(2)
    await sent.delete()
    
    

async def on_stream_ended(update, bot, vc):
    try:
        played = await play_next_song(bot, update.chat_id, vc)
    except Exception as e:
        raise e
    
    print(played)
        
              