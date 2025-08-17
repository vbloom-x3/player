# Player - A Music Player

Welcome to **Player**, a lightweight, terminal-based music player made with love in Python! Perfect for vibing to your favorite `.flac` tracks with a CLI interface.

---

##  Features

* Play high-quality audio (`.flac`) right from your terminal
* Simple and intuitive CLI controls
* Easy setup and installation
* Based on libVLC

---

##  Requirements

Make sure you have **fzf** installed!

```bash
# for Arch Linux-based distros
sudo pacman -S fzf
```

Make sure you have **Python 3** installed! Then install the dependencies:

```bash
pip install -r requirements.txt
```

**Suggested dependencies:**

```
python-vlc
mutagen
```

---

## Installation

You can run it directly, or “install” it to make it callable from anywhere:

```bash
make install-player
```

Then just type:

```bash
player
```

…and enjoy your music!

---

## Usage

* Run the player:

```bash
make run
```

* Or if installed in your PATH:

```bash
player
```

* Add your tracks to any folder in your home directory.

---


