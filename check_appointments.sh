#!/bin/bash
export DISPLAY=:0
export PATH=$PATH:/usr/local/bin:/Users/ggarcia/bin:/Users/ggarcia/.local/bin

cd /Users/ggarcia/Dropbox_Projects/Personal/make-appointment
poetry run python make_appointment/__init__.py
