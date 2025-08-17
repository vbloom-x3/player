#!/usr/bin/env bash

fd . ~ -e flac | fzf | python /home/$USER/.local/bin/player.py
