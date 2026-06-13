# backend/agents/base.py
"""Base agent with shared LLM client, RAG, and tool calling."""

import json
import logging
from typing import List, Optional

from openai import OpenAI

from backend.config import settings
from backend.tools.registry import tool_registry

logger = logging.getLogger(__name__)


class BaseAgent:
    """Shared functionality for all agents."""

    def __init__(self, system_prompt: str):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.DEFAULT_MODEL
        self.system_prompt = system_prompt

    def _chat(self, user_message: str, max_tokens: int = 1000, temperature: float = 0.7) -> dict:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens if response.usage else 0
        return {"content": content, "tokens_used": tokens}

    def _chat_with_tools(
        self,
        user_message: str,
        max_tokens: int = 1500,
        temperature: float = 0.3,
        max_iterations: Optional[int] = None,
    ) -> dict:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message},
        ]
        tools = tool_registry.get_openai_tools()
        total_tokens = 0
        tool_calls_made = []
        iterations = max_iterations or settings.MAX_TOOL_ITERATIONS

        for _ in range(iterations):
            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages,
            }
            if tools and settings.ENABLE_TOOLS:
                kwargs["tools"] = tools
                kwargs["tool_choice"] = "auto"

            response = self.client.chat.completions.create(**kwargs)
            total_tokens += response.usage.total_tokens if response.usage else 0
            choice = response.choices[0]

            if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
                messages.append(choice.message)
                for tool_call in choice.message.tool_calls:
                    args = json.loads(tool_call.function.arguments)
                    result = tool_registry.execute(tool_call.function.name, args)
                    tool_calls_made.append({
                        "tool": tool_call.function.name,
                        "arguments": args,
                        "result": result[:500],
                    })
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })
            else:
                return {
                    "content": choice.message.content or "",
                    "tokens_used": total_tokens,
                    "tool_calls": tool_calls_made,
                }

        return {
            "content": messages[-1].get("content", "") if isinstance(messages[-1], dict) else "",
            "tokens_used": total_tokens,
            "tool_calls": tool_calls_made,
        }

    @staticmethod
    def build_rag_context(knowledge: str, user_context: Optional[str] = None) -> str:
        parts = []
        if knowledge:
            parts.append(f"Relevant knowledge from documentation:\n{knowledge}")
        if user_context:
            parts.append(f"Project context:\n{user_context}")
        return "\n\n".join(parts)
