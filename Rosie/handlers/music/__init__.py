"""
Register all bot command handlers here.
"""
from pytgcalls import filters
from telethon import events
from core.events import MessageEvents, command_pattern
from .handles import (
    userbot_status,
    play,
    control_commands
)



def register(bot, userbot, vc):
    
    # ============================================================
    # play
    # ============================================================
    @bot.on(events.NewMessage(pattern=command_pattern("play|vplay")))
    @MessageEvents(group=True)
    async def play_command(event):
        await play.handle(event, userbot, vc)  
    
    
    # ============================================================
    # skip
    # ============================================================
    @bot.on(events.NewMessage(pattern=command_pattern("skip|end")))
    @MessageEvents(group=True, admins_only=True)
    async def skip_command(event):
        await control_commands.handle(event, vc)  
        
    
    # ============================================================
    # Raw Event on Usebot status change
    # ============================================================
    @userbot.on(events.Raw)
    async def _userbot_cache(event):
        await userbot_status.handle(event, bot)
    
    
    @vc.on_update()        
    async def on_stream_end(client, update):
        if "StreamEnded" in str(update):
            await control_commands.on_stream_ended(bot, vc)
        







