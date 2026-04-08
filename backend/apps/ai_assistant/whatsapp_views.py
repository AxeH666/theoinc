from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from apps.ai_assistant.services import handle_customer_query


@api_view(["POST"])
@permission_classes([AllowAny])
def whatsapp_webhook(request):
    phone = request.data.get("phone")
    message = (request.data.get("message") or "").strip()

    if not phone or not message:
        return Response(
            {"detail": "Both 'phone' and 'message' are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    customer_query, quotation_id = handle_customer_query(message)
    return Response(
        {
            "response": customer_query.response_text,
            "intent": customer_query.intent,
            "quotation_id": quotation_id,
        },
        status=status.HTTP_200_OK,
    )
