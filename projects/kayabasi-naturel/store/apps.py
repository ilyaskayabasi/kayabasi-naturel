import os

from django.apps import AppConfig
from django.core.management import call_command
from django.db import connection
from django.db.utils import OperationalError


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        # Production safety net: auto-run migrations if core tables are missing.
        # Can be disabled via AUTO_MIGRATE=0.
        if os.getenv('AUTO_MIGRATE', '1') != '1':
            return

        try:
            tables = connection.introspection.table_names()
            if 'store_product' not in tables:
                call_command('migrate', interactive=False, run_syncdb=True)
        except OperationalError:
            # DB not initialized yet: attempt migrate once.
            try:
                call_command('migrate', interactive=False, run_syncdb=True)
            except Exception:
                pass
        except Exception:
            # Swallow any unexpected error to avoid blocking app startup.
            pass
