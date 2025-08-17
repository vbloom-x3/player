# Default target
all: install run install force-i install-player

# Install dependencies
install:
	pip install -r requirements.txt

force-i:
	pip install -r requirements.txt --break-system-packages

install-player:
        chmod +x main.sh
	cp main.sh ~/.local/bin/player
        @echo "player              -> Run the music player"
# Run the player
run:
	fd . ~ -e flac | fzf | python3 src/main.py

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

help:
	@echo "make install        -> Install dependencies"
	@echo "make force-i        -> Add --break-system-packages to pip
	@echo "make install-player -> Install player"
	@echo "make run            -> Run the music player"
	@echo "make clean          -> Remove pycache and temporary files"
