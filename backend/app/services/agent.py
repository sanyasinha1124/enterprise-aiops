import json

from app.core.config import get_settings
from app.services.llm import GeminiService
from app.services.rag import RAGService
from app.services.tools import TOOL_FUNCTIONS


TOOL_SCHEMAS = [
    {
        "type": "function",
        "name": "get_customer",
        "description": "Get a customer by numeric customer ID.",
        "parameters": {
            "type": "object",
            "properties": {"customer_id": {"type": "integer"}},
            "required": ["customer_id"],
        },
    },
    {
        "type": "function",
        "name": "get_order",
        "description": "Get an order by numeric order ID.",
        "parameters": {
            "type": "object",
            "properties": {"order_id": {"type": "integer"}},
            "required": ["order_id"],
        },
    },
    {
        "type": "function",
        "name": "calculate_refund_eligibility",
        "description": "Check whether an order is inside the refund window.",
        "parameters": {
            "type": "object",
            "properties": {
                "days_since_purchase": {"type": "integer"},
                "refund_window_days": {"type": "integer"},
            },
            "required": ["days_since_purchase"],
        },
    },
    {
        "type": "function",
        "name": "create_support_ticket",
        "description": "Create a support ticket. Only use when the user explicitly asks to create one.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "integer"},
                "issue": {"type": "string"},
            },
            "required": ["customer_id", "issue"],
        },
    },
]


class AgentService:
    def __init__(self):
        settings = get_settings()
        self.settings = settings
        self.client_service = GeminiService()
        self.rag = RAGService()

    def run(self, question: str):
        # First retrieve enterprise knowledge.
        sources = self.rag.retrieve(question)

        context = "\n\n".join(
            f"[SOURCE {i+1}] {s['title']}\n{s['text']}"
            for i, s in enumerate(sources)
        )

        system = """
You are EnterpriseOps AI.
You are an enterprise operations assistant.
Use tools when private operational data is needed.
Use retrieved context for company policies.
Never invent database values.
Never create a support ticket unless the user explicitly asks.
Explain what you found and cite retrieved documents as [SOURCE N].
"""

        prompt = f"""
RETRIEVED KNOWLEDGE:
{context}

USER QUESTION:
{question}
"""

        # The direct Gemini Interactions API is used here so the tool-calling loop
        # is visible for learning rather than hidden behind a framework.
        client = self.client_service.client

        interaction = client.interactions.create(
            model=self.settings.gemini_model,
            input=f"{system}\n\n{prompt}",
            tools=TOOL_SCHEMAS,
        )

        tool_calls = []
        previous_id = interaction.id

        for step in interaction.steps:
            if getattr(step, "type", None) != "function_call":
                continue

            name = step.name
            args = step.arguments
            if isinstance(args, str):
                args = json.loads(args)

            if name not in TOOL_FUNCTIONS:
                continue

            # Explicit allow-list: the model cannot execute arbitrary Python.
            result = TOOL_FUNCTIONS[name](**args)
            tool_calls.append(
                {"tool": name, "arguments": args, "result": result}
            )

            followup = client.interactions.create(
                model=self.settings.gemini_model,
                previous_interaction_id=previous_id,
                input=[
                    {
                        "type": "function_result",
                        "name": name,
                        "call_id": step.id,
                        "result": [
                            {"type": "text", "text": json.dumps(result)}
                        ],
                    }
                ],
            )
            previous_id = followup.id
            interaction = followup

        return interaction.output_text or "", sources, tool_calls
