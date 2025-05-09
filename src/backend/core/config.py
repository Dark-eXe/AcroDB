import os

# Base path to src/
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Path to prompt
PROMPT_PATH = os.path.join(SRC_DIR, "AcroDB", "prompts", "main.txt")

CORS_CONFIG = {
    "allow_origins": ["*"],  # Allow all origins
    "allow_credentials": True,
    "allow_methods": ["*"],  # Allow all methods (GET, POST, etc.)
    "allow_headers": ["*"],  # Allow all headers
}