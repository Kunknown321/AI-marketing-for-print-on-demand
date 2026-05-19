"""Unified AI client supporting multiple free/paid LLM providers."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class AIClient:
    """Unified client for LLM interactions. Supports OpenAI and compatible APIs."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model or os.getenv("MODEL_NAME", "gpt-4")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self._client = None

    @property
    def client(self):
        if self._client is None:
            from openai import OpenAI

            kwargs = {"api_key": self.api_key}
            if self.base_url:
                kwargs["base_url"] = self.base_url
            self._client = OpenAI(**kwargs)
        return self._client

    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        json_mode: bool = False,
    ) -> str:
        """Generate a response from the AI model.

        Args:
            prompt: User prompt.
            system_prompt: System prompt for context.
            temperature: Creativity level (0.0 - 1.0).
            max_tokens: Maximum response length.
            json_mode: Whether to request JSON output.

        Returns:
            Generated text response.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    def generate_json(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> dict:
        """Generate a JSON response from the AI model.

        Args:
            prompt: User prompt.
            system_prompt: System prompt for context.
            temperature: Creativity level.
            max_tokens: Maximum response length.

        Returns:
            Parsed JSON dictionary.
        """
        text = self.generate(
            prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            json_mode=True,
        )
        return json.loads(text)
