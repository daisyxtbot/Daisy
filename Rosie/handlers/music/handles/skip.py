import asyncio
from ..utils.play_handle import play_next_song





async def handle(event, vc):

    try:
        await play_next_song(event, vc)
        sent = await event.reply(event.get_reply("skipping"))
    except Exception as e:
        if "bot not streaming" in str(e):
            await event.reply(event.get_reply("bot_not_streaming"))
        else:
            await event.reply(f"{e}")
        return    
    
    await sent.edit(event.get_reply("skipped"))
    
    await asyncio.sleep(2)
    await sent.delete()
        