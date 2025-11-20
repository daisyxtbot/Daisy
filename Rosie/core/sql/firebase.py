import aiohttp
import asyncio
from core.clients.config import FIREBASE_URL  # FIREBASE_URL = "https://daisyxtbot-5e032-default-rtdb.asia-southeast1.firebasedatabase.app"

# -----------------------------
# Helper to build full URL
# -----------------------------
def _build_url(path):
    return f"{FIREBASE_URL.rstrip('/')}/{path.lstrip('/')}.json"

# -----------------------------
# GET method (awaitable, returns JSON)
# -----------------------------
async def get(path):
    url = _build_url(path)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.json()

# -----------------------------
# PATCH method (fire-and-forget)
# -----------------------------
async def _patch_task(url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=payload) as resp:
            resp.raise_for_status()
            return await resp.json()

async def patch(path, data: dict):
    """
    Fire-and-forget PATCH.
    - data: dict or normal value
    """
    url = _build_url(path)
    asyncio.create_task(_patch_task(url, data))

# -----------------------------
# DELETE method (fire-and-forget)
# -----------------------------
async def _delete_task(url):
    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as resp:
            resp.raise_for_status()
            return await resp.json()

async def delete(path):
    """Fire-and-forget DELETE"""
    url = _build_url(path)
    asyncio.create_task(_delete_task(url))