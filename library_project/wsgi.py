"""
WSGI config for library_project project.

On Vercel, the SQLite database lives in /tmp and is wiped on cold starts.
We run migrations automatically here so the app is always ready.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')

# Auto-run migrations on startup (essential for Vercel's ephemeral /tmp SQLite)
try:
    from django.core.management import call_command
    call_command('migrate', '--run-syncdb', verbosity=0, interactive=False)
except Exception:
    pass  # If it fails, let the app still try to start

application = get_wsgi_application()
