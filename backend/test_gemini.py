#!/usr/bin/env python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load .env
from dotenv import load_dotenv
load_dotenv('../.env')

from app.services.gemini_service import get_gemini_service
import asyncio

async def test():
    service = get_gemini_service()
    print(f"Model name: {service.model_name}")
    try:
        result = await service.call_gemini('Say hello in one sentence.', max_tokens=50)
        print('SUCCESS:', result[:200] if result else 'Empty response')
    except Exception as e:
        print('ERROR:', type(e).__name__, str(e))

if __name__ == "__main__":
    asyncio.run(test())
