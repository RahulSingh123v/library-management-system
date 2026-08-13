#!/bin/bash
# Vercel build script — runs during static-build phase
python3.12 -m pip install -r requirements.txt
python3.12 manage.py collectstatic --noinput
