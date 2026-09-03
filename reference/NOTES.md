# Normative References

AI Periscope consumes the NeoMundi Runtime Measurement Layer; it does not
vendor or reimplement it. This file points to the sources this product's
vocabulary, boundaries, and client behavior are aligned with, and summarizes
what was carried into the codebase from each — it does not reproduce those
documents.

| Source | Repository | What Periscope takes from it |
|---|---|---|
| NeoMundi Runtime Measurement Layer | `neomundi-runtime-measurement` | API integration flow (3 steps), field vocabulary (`periscope/measurement/contracts.py`), consumer boundaries (`docs/METRIC_BOUNDARIES.md`) |
| NeoMundi Measurement Interoperability | `neomundi-measurement-interoperability` | RGC v0.1/v0.2 semantics (schema_version matching, per-signal `signal_status`, coverage consistency), the reference consumer's verification flow as a structural model (not copied code) |
| NeoMundi Metric Contract | `neomundi-metric-contract` | Signal definitions and limits (`stability_score`, `coherence_score`, `factual_validity_signal`, `semantic_variability_signal`, `risk_signal`) |

## Provider list

The provider registry (`periscope/providers/registry.py`) is sourced
verbatim from the NeoMundi Runtime Measurement Layer's
`API_INTEGRATION_GUIDE.md`, section 3.1 ("Supported providers," per
`resolve_provider_key()` in NeoMundi's reference client):

```text
openai · anthropic · google (alias gemini) · mistral · cohere · deepseek
xai (alias grok) · perplexity · together · qwen · apertus · euria
```

Periscope does not claim support for a provider NeoMundi has not documented.

## What is deliberately not vendored here

- The full RGC v0.1/v0.2 JSON Schemas and NeoMundi's published reference
  verifier (hash + Ed25519/JWS signature verification) are not copied into
  this repository. `periscope/measurement/contracts.py` implements
  structural validation only (schema-version matching, coverage
  consistency) — sufficient to keep Periscope from misinterpreting a
  contract, but not a substitute for full schema validation or
  cryptographic verification in a production integration. Consult the
  NeoMundi Measurement Interoperability repository directly for that.
- No official NeoMundi thresholds exist to vendor: NeoMundi's own consumer
  boundaries document states explicitly that it publishes no official
  numeric thresholds. Any threshold in this product (e.g.
  `periscope/analysis/audit.py`'s `AuditThresholds`) is a Periscope-side
  configuration default, documented as such wherever it appears.

## Private methodological reference

NeoMundi's private Euria/Fatima reporting generator (not part of this
repository) informed the shape of the analysis library and the two open
reports — see the root `README.md` for what was generalized from it and
what was intentionally left out.
