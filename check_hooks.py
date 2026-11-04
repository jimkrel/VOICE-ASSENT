import os
import re

APP_PATH = r"E:\VoiceAI\studio_app.py"

with open(APP_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Let's inspect specific hooks in content
print(f"File loaded: {len(content)} characters")

has_tts = "def tts(" in content
has_run_single = "def _run_single(" in content
has_status = "def status_html(" in content
has_quote = "def render_voice_preview_quote(" in content

print(f"Hooks found: tts={has_tts}, run_single={has_run_single}, status={has_status}, quote={has_quote}")
