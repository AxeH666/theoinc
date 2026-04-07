from django.conf import settings

import requests

from apps.ai_assistant.models import CustomerQuery, CustomerQueryIntent
from apps.ai_assistant.rag import search_knowledge
from apps.customers.models import Customer


GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)


INTENT_KEYWORDS = {
    CustomerQueryIntent.QUOTATION_REQUEST: [
        "quote",
        "quotation",
        "price",
        "cost",
        "how much",
    ],
    CustomerQueryIntent.SERVICE_REQUEST: [
        "repair",
        "fix",
        "maintenance",
        "not working",
        "broken",
    ],
    CustomerQueryIntent.PRODUCT_INQUIRY: [
        "what is",
        "tell me about",
        "explain",
        "how does",
    ],
}


def detect_intent(query_text):
    normalized_query = query_text.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in normalized_query for keyword in keywords):
            return intent
    return CustomerQueryIntent.GENERAL


def build_context_block(context_chunks):
    if not context_chunks:
        return "No indexed knowledge base context was found."
    return "\n\n".join(
        f"Context {index}: {chunk}" for index, chunk in enumerate(context_chunks, start=1)
    )


def generate_gemini_response(query_text, context_chunks):
    if not settings.GEMINI_API_KEY:
        return "AI assistant is not configured yet. Please add a valid GEMINI_API_KEY."

    prompt = (
        "You are the AI assistant for theoinc, a solar energy business OS for "
        "Incetekh Energy Solutions. Answer clearly and helpfully using the provided "
        "knowledge context when it is relevant. If the context is incomplete, say so "
        "briefly and avoid inventing details.\n\n"
        f"Knowledge context:\n{build_context_block(context_chunks)}\n\n"
        f"Customer query:\n{query_text}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt,
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(
            GEMINI_API_URL,
            params={"key": settings.GEMINI_API_KEY},
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        candidates = data.get("candidates", [])
        if not candidates:
            return "I could not generate a response at the moment."
        parts = candidates[0].get("content", {}).get("parts", [])
        text_parts = [part.get("text", "") for part in parts if part.get("text")]
        if text_parts:
            return "\n".join(text_parts).strip()
    except requests.RequestException:
        return "The AI assistant is temporarily unavailable. Please try again shortly."

    return "I could not generate a response at the moment."


def handle_customer_query(query_text, customer_id=None):
    context_chunks = search_knowledge(query_text)
    intent = detect_intent(query_text)
    response_text = generate_gemini_response(query_text, context_chunks)

    customer = None
    if customer_id:
        customer = Customer.objects.filter(pk=customer_id).first()

    return CustomerQuery.objects.create(
        customer=customer,
        query_text=query_text,
        intent=intent,
        response_text=response_text,
    )
