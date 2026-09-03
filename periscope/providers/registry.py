"""Provider registry.

Lists only providers documented by NeoMundi's own integration guide
(`resolve_provider_key()` in the NeoMundi reference client, per
API_INTEGRATION_GUIDE.md section 3.1). Periscope does not hardcode provider
logic in the core engine, and does not claim support for a provider that
NeoMundi has not documented.

If NeoMundi documents additional providers in the future, add them here --
this is the single place the rest of the codebase should look.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderInfo:
    key: str
    aliases: tuple[str, ...] = ()
    api_key_env: str = ""  # environment variable Periscope reads for this provider's key


_PROVIDERS: dict[str, ProviderInfo] = {
    info.key: info
    for info in (
        ProviderInfo("openai", api_key_env="PERISCOPE_OPENAI_API_KEY"),
        ProviderInfo("anthropic", api_key_env="PERISCOPE_ANTHROPIC_API_KEY"),
        ProviderInfo("google", aliases=("gemini",), api_key_env="PERISCOPE_GOOGLE_API_KEY"),
        ProviderInfo("mistral", api_key_env="PERISCOPE_MISTRAL_API_KEY"),
        ProviderInfo("cohere", api_key_env="PERISCOPE_COHERE_API_KEY"),
        ProviderInfo("deepseek", api_key_env="PERISCOPE_DEEPSEEK_API_KEY"),
        ProviderInfo("xai", aliases=("grok",), api_key_env="PERISCOPE_XAI_API_KEY"),
        ProviderInfo("perplexity", api_key_env="PERISCOPE_PERPLEXITY_API_KEY"),
        ProviderInfo("together", api_key_env="PERISCOPE_TOGETHER_API_KEY"),
        ProviderInfo("qwen", api_key_env="PERISCOPE_QWEN_API_KEY"),
        ProviderInfo("apertus", api_key_env="PERISCOPE_APERTUS_API_KEY"),
        ProviderInfo("euria", api_key_env="PERISCOPE_EURIA_API_KEY"),
    )
}

_ALIAS_TO_KEY: dict[str, str] = {
    alias: info.key for info in _PROVIDERS.values() for alias in info.aliases
}


class UnknownProviderError(ValueError):
    pass


def resolve_provider(name: str) -> ProviderInfo:
    """Resolve a provider name or alias (case-insensitive) to its ProviderInfo.

    Raises UnknownProviderError for anything not documented by NeoMundi --
    Periscope must not silently accept an unsupported provider name.
    """
    normalized = name.strip().lower()
    if normalized in _PROVIDERS:
        return _PROVIDERS[normalized]
    if normalized in _ALIAS_TO_KEY:
        return _PROVIDERS[_ALIAS_TO_KEY[normalized]]
    raise UnknownProviderError(
        f"Unsupported provider {name!r}. Supported providers: "
        f"{', '.join(sorted(_PROVIDERS))} (see docs/CAMPAIGN_MODEL.md)."
    )


def list_providers() -> tuple[str, ...]:
    return tuple(sorted(_PROVIDERS))
