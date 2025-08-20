import vlc
import time
import shutil
from mutagen.flac import FLAC
import os


def get_flac_metadata(audio_file):
    """
    Fetch FLAC metadata for the given file.
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
    Convert milliseconds to M:SS.
    """
    if ms <= 0:
        return "0:00"
    seconds = int(ms / 1000)
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"


class GaplessPlayer:
    def __init__(self, playlist=None, display_progress=True):
        self.playlist = playlist or []
        self.display_progress = display_progress
        self.player = vlc.MediaPlayer()
        self.current_index = 0
        self.event_manager = self.player.event_manager()
        self.event_manager.event_attach(
            vlc.EventType.MediaPlayerEndReached, self._on_track_end
        )

    def _on_track_end(self, event):
        self.current_index += 1
        if self.current_index < len(self.playlist):
            self._play_current()
        else:
            print("\nPlaylist completed!")

    def _play_current(self):
        track = self.playlist[self.current_index]
        if not os.path.exists(track):
            print(f"File not found: {track}")
            return
        metadata = get_flac_metadata(track)
        print(f"\nNow playing: {metadata['full_title']}")
        self.player.set_media(vlc.Media(track))
        self.player.play()

    def play_all(self):
        if not self.playlist:
            print("Playlist is empty!")
            return
        self._play_current()
        self._progress_loop()

    def _progress_loop(self):
        last_progress_line = ""
        while True:
            state = self.player.get_state()
            if state == vlc.State.Ended and self.current_index >= len(self.playlist) - 1:
                break
            if state in [vlc.State.Error, vlc.State.Stopped]:
                break

            if self.display_progress:
                current = self.player.get_time()
                total = self.player.get_length()
                if total <= 0:
                    total = 1
                progress = min(current / total, 1.0)
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
        print("\nPlayback completed!")
