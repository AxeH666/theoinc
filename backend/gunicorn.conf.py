import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django  # noqa: E402

django.setup()

from django.conf import settings  # noqa: E402

# Disable Gunicorn's default handlers (stdout/stderr); logconfig_dict replaces them
errorlog = "-"
accesslog = "-"
loglevel = "info"
capture_output = True
timeout = 300
workers = 1


def post_fork(server, worker):
    try:
        from apps.ai_assistant.rag import get_embedding_model

        get_embedding_model()
        print("Embedding model pre-loaded successfully")
    except Exception as e:
        print(f"Could not pre-load embedding model: {e}")

# Gunicorn applies dictConfig; Django's LOGGING replaces its handlers
logconfig_dict = settings.LOGGING
