import asyncio
import random

async def human_delay(a=2, b=5):
    await asyncio.sleep(random.uniform(a, b))
