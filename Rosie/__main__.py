import asyncio
from quart import Quart
from core.clients import start_clients
from handlers import register_clients

"""
main() is the entry point of your program.
It will start both: bot + userbot (inside start_clients)
"""
app = Quart(__name__)

@app.get("/")
async def home():
    return {"status": "✅ Bot is running smoothly!"}


async def main():
    # Start bot + userbot + pytgcalls in background
    asyncio.create_task(start_clients())
    
    # Start Quart (this blocks event loop)
    await app.run_task(host="0.0.0.0", port=5000)


    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()