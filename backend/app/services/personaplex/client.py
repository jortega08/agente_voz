"""
Conversation client powered by OpenAI GPT.

Replaces the local PersonaPlex model with the OpenAI Chat Completions API,
maintaining the same interface and using the existing prompt templates.
"""

import structlog
from openai import AsyncOpenAI

from app.config import get_settings
from app.services.personaplex.prompts import SYSTEM_PROMPT, STRATEGY_PROMPTS, EMOTIONAL_RESPONSE_GUIDES

logger = structlog.get_logger()


class PersonaPlexClient:
    def __init__(self):
        self.settings = get_settings()
        self._client: AsyncOpenAI | None = None

    def _get_client(self) -> AsyncOpenAI:
        if self._client is None:
            self._client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        return self._client

    def _build_system_prompt(self, persona_config: dict | None) -> str:
        config = persona_config or {}
        base = SYSTEM_PROMPT.replace("${original_amount}", str(config.get("original_amount", "N/A")))
        base = base.replace("${negotiable_amount}", str(config.get("negotiable_amount", "N/A")))
        base = base.replace("${days_past_due}", str(config.get("days_past_due", "N/A")))
        strategy = config.get("strategy", "empathetic")
        base = base.replace("${strategy}", strategy)

        strategy_guide = STRATEGY_PROMPTS.get(strategy, "")
        emotional_state = config.get("emotional_state", "cooperative")
        emotional_guide = EMOTIONAL_RESPONSE_GUIDES.get(emotional_state, "")

        return f"{base}\n\n{strategy_guide}\n\n{emotional_guide}"

    async def generate_text_response(
        self,
        text_input: str,
        persona_config: dict | None = None,
        conversation_history: list[dict] | None = None,
    ) -> str:
        """
        Generate a text response using OpenAI GPT.

        Args:
            text_input: Transcribed user text.
            persona_config: Agent persona configuration (strategy, amounts, emotional_state).
            conversation_history: Previous turns as list of {"role": ..., "content": ...}.

        Returns:
            Agent response text.
        """
        client = self._get_client()
        system_prompt = self._build_system_prompt(persona_config)

        messages = [{"role": "system", "content": system_prompt}]
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": text_input})

        try:
            response = await client.chat.completions.create(
                model=self.settings.openai_model,
                messages=messages,
                temperature=0.7,
                max_tokens=300,
            )
            reply = response.choices[0].message.content.strip()
            logger.info("openai_response_generated", tokens=response.usage.total_tokens)
            return reply

        except Exception as e:
            logger.error("openai_error", error=str(e))
            return "I understand your concern. Let me help you find the best solution for your situation."
