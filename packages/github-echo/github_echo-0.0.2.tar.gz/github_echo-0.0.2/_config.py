import os
from os.path import abspath, dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(abspath(__file__)), ".env")

# Check if the .env file exists before trying to load it
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Load environment variables
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
GITHUB_API_VERSION = os.getenv("GITHUB_API_VERSION")

# Optional: Print a warning if required environment variables are missing
if not GOOGLE_GEMINI_API_KEY:
    print("Warning: GOOGLE_GEMINI_API_KEY not found.")
if not GITHUB_API_TOKEN:
    print("Warning: GITHUB_API_TOKEN not found.")
if not GITHUB_API_VERSION:
    print("Warning: GITHUB_API_VERSION not found.")
