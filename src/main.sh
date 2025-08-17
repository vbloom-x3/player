#!/usr/bin/env bash

fd . ~ -e flac | fzf | python main.py
