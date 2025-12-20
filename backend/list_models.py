#!/usr/bin/env python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load .env
from dotenv import load_dotenv
load_dotenv('../.env')

import google.generativeai as genai

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key present: {bool(api_key)}")
print(f"API Key (first 10 chars): {api_key[:10] if api_key else 'None'}...")

genai.configure(api_key=api_key)

print("\nAvailable models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")
