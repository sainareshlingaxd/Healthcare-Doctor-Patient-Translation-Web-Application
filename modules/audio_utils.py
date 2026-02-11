
import os
import uuid

AUDIO_DIR = "audio_files"

if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

def save_audio(audio_bytes):
    """
    Save audio bytes to a file and return the path.
    """
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join(AUDIO_DIR, filename)
    
    with open(filepath, "wb") as f:
        f.write(audio_bytes)
    
    return filepath
