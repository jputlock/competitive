#!/usr/bin/bash

vars=$@
tmux new-session -s advent "python3 launcher.py $vars"