#!/usr/bin/env bash

fd . ~ -e wav | fzf | python /home/$USER/.local/bin/player-wav.py
