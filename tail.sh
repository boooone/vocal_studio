#!/bin/bash

ABLETON_LOG_FILE="/mnt/c/Users/jtboo/AppData/Roaming/Ableton/Live 12.1.5/Preferences/Log.txt"
cat "$ABLETON_LOG_FILE"
tail -f ---disable-inotify "$ABLETON_LOG_FILE"
