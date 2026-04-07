from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.ai_assistant.views import CustomerQueryViewSet, KnowledgeBaseViewSet, chat

app_name = "ai_assistant"

router = DefaultRouter()
router.register(r"queries", CustomerQueryViewSet, basename="customer-query")
router.register(r"knowledge-base", KnowledgeBaseViewSet, basename="knowledge-base")

urlpatterns = [
    path("chat/", chat, name="chat"),
]
urlpatterns += router.urls
