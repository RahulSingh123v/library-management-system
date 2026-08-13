#!/bin/bash
# Vercel build script — installs dependencies and collects static files

# PEP 668: Vercel's system Python requires --break-system-packages flag
python3.12 -m pip install -r requirements.txt --break-system-packages

# Collect static files into staticfiles/
python3.12 manage.py collectstatic --noinput
