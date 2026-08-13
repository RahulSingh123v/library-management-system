"""
WSGI config for library_project project.

On Vercel, the SQLite database lives in /tmp and is wiped on cold starts.
We run migrations automatically here so the app is always ready.
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')

# Initialize Django WSGI application first
application = get_wsgi_application()
app = application  # Required for Vercel serverless functions

# Auto-run migrations and seeding on startup after Django is fully initialized
try:
    from django.core.management import call_command
    sys.stderr.write("Running auto-migrations on Vercel startup...\n")
    call_command('migrate', '--run-syncdb', verbosity=0, interactive=False)
    sys.stderr.write("Auto-migrations completed successfully.\n")
    
    # Run database seed
    from library.seed import seed_database
    sys.stderr.write("Running database seeding...\n")
    seed_database()
except Exception as e:
    sys.stderr.write(f"Auto-migration/seed failed: {str(e)}\n")
