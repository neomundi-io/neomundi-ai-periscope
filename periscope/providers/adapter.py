"""Maps a Periscope provider/model arm to what NeoMundi's API expects, and
resolves the provider API key from the environment.

No provider-specific request logic lives here: NeoMundi's /v1/govern/stream
takes the same {prompt, provider, model, provider_api_key} shape for every
documented provider (API_INTEGRATION_GUIDE.md section 3).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from periscope.providers.registry import resolve_provider


@dataclass(frozen=True)
class ProviderModelArm:
    """One (provider, model) pair a campaign runs against."""

    provider: str
    model: str

    @property
    def arm_id(self) -> str:
        return f"{self.provider}:{self.model}"


def resolve_provider_api_key(provider: str) -> str | None:
    """Read the provider's API key from its dedicated environment variable.

    Returns None (never an empty string masquerading as a key) if unset --
    callers must decide how to handle a missing key; this function does not.
    """
    info = resolve_provider(provider)
    value = os.getenv(info.api_key_env)
    return value or None


def build_govern_stream_payload(prompt: str, arm: ProviderModelArm, provider_api_key: str) -> dict:
    """Build the request body for POST /v1/govern/stream.

    Deliberately omits temperature/top_p/seed: API_INTEGRATION_GUIDE.md
    documents this as an observed operational rule -- each provider is
    measured under its native default generation policy unless NeoMundi
    confirms otherwise.
    """
    resolve_provider(arm.provider)  # raises UnknownProviderError if not documented
    return {
        "prompt": prompt,
        "model": arm.model,
        "provider": arm.provider,
        "provider_api_key": provider_api_key,
    }
