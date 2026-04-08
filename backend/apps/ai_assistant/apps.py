from django.apps import AppConfig


class AiAssistantConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ai_assistant"

    def ready(self):
        try:
            from .rag import get_embedding_model

            get_embedding_model()
            print("Embedding model pre-loaded")
        except Exception as e:
            print(f"Could not pre-load embedding model: {e}")
