# Default target
all: install run req

# Install dependencies
req:
	pip install -r requirements.txt

# Run the player
run:
	fd . ~ -e flac | fzf | python3 src/main.py

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

help:
	@echo "make install  -> Install dependencies"
	@echo "make run      -> Run the music player"
	@echo "make clean    -> Remove pycache and temporary files"
