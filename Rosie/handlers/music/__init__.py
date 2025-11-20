"""
Register all bot command handlers here.
"""
from telethon import events
from core.events import MessageEvents, command_pattern
from .handles import (
    userbot_status,
    play,
    skip
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
    @bot.on(events.NewMessage(pattern=command_pattern("skip")))
    @MessageEvents(group=True, admins_only=True)
    async def skip_command(event):
        await skip.handle(event, vc)  
        
    
    # ============================================================
    # Raw Event on Usebot status change
    # ============================================================
    @userbot.on(events.Raw)
    async def _userbot_cache(event):
        await userbot_status.handle(event, bot)
            
            
        
        







