import vlc
import time
import shutil
from mutagen.flac import FLAC
import sys
import os


def get_flac_metadata(audio_file):
    """
    Fetch FLAC metadata for the given file.
    
    Returns:
        dict: {title, artist, album, full_title}
    """
    audio = FLAC(audio_file)
    title = audio.get("title", ["Unknown Title"])[0]
    artist = audio.get("artist", ["Unknown Artist"])[0]
    album = audio.get("album", ["Unknown Album"])[0]
    full_title = f"{album} -> {title} — {artist}"
    
    return {
        "title": title,
        "artist": artist,
        "album": album,
        "full_title": full_title
    }


def format_time(ms):
    """
    Format milliseconds to M:SS.
    """
    if ms <= 0:
        return "0:00"
    seconds = int(ms / 1000)
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"


def play_audio(audio_file, display_progress=True):
    """
    Play a FLAC audio file using VLC.
    
    Args:
        audio_file (str): Path to the FLAC file.
        display_progress (bool): Whether to show progress bar in terminal.
    """
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"File not found: {audio_file}")
    
    metadata = get_flac_metadata(audio_file)
    print(f"Now playing: {metadata['full_title']}")
    
    # Initialize VLC player
    player = vlc.MediaPlayer(audio_file)
    player.play()
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
            state = player.get_state()
            if state in [vlc.State.Ended, vlc.State.Error]:
                break
            
            current = player.get_time()
            progress = min(current / total, 1.0) if total > 0 else 0
            
            if display_progress:
                width = shutil.get_terminal_size().columns
                bar_width = max(width - 30, 10)
                filled = int(progress * bar_width)
                bar = "=" * filled + " " * (bar_width - filled)
                
                progress_text = f"[{bar}] {int(progress*100)}% | {format_time(current)}/{format_time(total)}"
                
                if len(progress_text) > width:
                    progress_display = progress_text[:width]
                else:
                    progress_display = progress_text.ljust(width)
                
                if progress_display != last_progress_line:
                    print(f"\r{progress_display}", end='', flush=True)
                    last_progress_line = progress_display
            
            time.sleep(0.05)
        
        if display_progress:
            print()  # Move to next line
        print("Playback completed!")
    
    except KeyboardInterrupt:
        print("\nStopped!")
    
    except Exception as e:
        print(f"\nError: {e}")
    
    finally:
        player.stop()


def main():
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        audio_file = sys.stdin.readline().strip()
    
    play_audio(audio_file)


if __name__ == "__main__":
    main()
