import vlc
import time
import shutil
from mutagen.flac import FLAC
import sys
import os

# Read file from argument or stdin
if len(sys.argv) > 1:
    audio_file = sys.argv[1]
else:
    audio_file = sys.stdin.readline().strip()

if not os.path.exists(audio_file):
    print("File not found!")
    sys.exit(1)

# Fetch metadata
audio = FLAC(audio_file)
title = audio.get("title", ["Unknown Title"])[0]
artist = audio.get("artist", ["Unknown Artist"])[0]
album = audio.get("album", ["Unknown Album"])[0]
full_title = f"{album} -> {title} — {artist}"

# Print initial info (only once)
print(f"Now playing: {full_title}")

# VLC player
player = vlc.MediaPlayer(audio_file)
player.play()
time.sleep(0.5)  # give VLC time to parse

def format_time(ms):
    if ms <= 0:
        return "0:00"
    seconds = int(ms / 1000)
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"

# Wait until VLC reports a valid length
total = player.get_length()
retry_count = 0
while total <= 0 and retry_count < 50:
    time.sleep(0.1)
    total = player.get_length()
    retry_count += 1

if total <= 0:
    total = 1  # Prevent division by zero

try:
    last_progress_line = ""
    
    while True:
        # Check if player is still valid
        state = player.get_state()
        if state in [vlc.State.Ended, vlc.State.Error]:
            break
            
        width = shutil.get_terminal_size().columns
        current = player.get_time()
        
        # Prevent division by zero
        if total > 0:
            progress = min(current / total, 1.0)
        else:
            progress = 0
        
        # Bar width calculation
        bar_width = max(width - 30, 10)
        filled = int(progress * bar_width)
        bar = "=" * filled + " " * (bar_width - filled)

        # Create progress line
        progress_text = f"[{bar}] {int(progress*100)}% | {format_time(current)}/{format_time(total)}"
        
        # Truncate or pad to exact width
        if len(progress_text) > width:
            progress_display = progress_text[:width]
        else:
            progress_display = progress_text.ljust(width)
        
        # Update progress line (overwrite current line)
        if progress_display != last_progress_line:
            print(f"\r{progress_display}", end='', flush=True)
            last_progress_line = progress_display

        time.sleep(0.05)

    # Print final newline and completion message
    print()  # Move to next line
    print("Playback finished!")

except KeyboardInterrupt:
    print()  # Move to next line
    print("Stopped!")
except Exception as e:
    print()  # Move to next line
    print(f"Error: {e}")
finally:
    player.stop()
