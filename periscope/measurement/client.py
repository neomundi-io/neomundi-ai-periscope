"""Real NeoMundi ControlTower client: the 3-step measurement flow.

Implements the flow documented in the NeoMundi Runtime Measurement Layer's
API_INTEGRATION_GUIDE.md:

    1. POST /v1/govern/stream  -- NeoMundi calls the provider on your behalf
    2. POST /v1/govern         -- full measurement
    3. POST /v1/rgc/contracts/{request_id} -- optional signed proof

Step 3 failures never fail the whole observation (per the guide's explicit
recommendation): the measurement from steps 1-2 remains valid without a
signed proof for that particular observation.

This module does not reimplement NeoMundi's measurement logic -- it only
calls the API and hands the response to `periscope.measurement.runtime` for
normalization.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass

import requests

from periscope.measurement.contracts import MeasurementRecord
from periscope.measurement.runtime import (
    build_measurement_record,
    extract_stream_final_text,
    extract_stream_latency_ms,
    extract_stream_token_count,
)
from periscope.providers.adapter import ProviderModelArm, build_govern_stream_payload

DEFAULT_BASE_URL = "https://api.neomundi.io"


@dataclass
class MeasurementResult:
    measurement: MeasurementRecord | None
    latency_ms: float | None
    token_count: int | None
    rgc_contract: dict | None
    error: str | None


class NeoMundiApiError(RuntimeError):
    pass


class NeoMundiControlTowerClient:
    """Talks to api.neomundi.io. Requires a NeoMundi API key and, per arm,
    the corresponding provider API key (see providers.adapter)."""

    def __init__(
        self,
        neomundi_api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        fetch_signed_contract: bool = False,
        timeout_s: int = 300,
        max_retries: int = 5,
    ) -> None:
        if not neomundi_api_key:
            raise ValueError("A NeoMundi API key is required.")
        self.neomundi_api_key = neomundi_api_key
        self.base_url = base_url.rstrip("/")
        self.fetch_signed_contract = fetch_signed_contract
        self.timeout_s = timeout_s
        self.max_retries = max_retries

    # -- retry policy, per API_INTEGRATION_GUIDE.md section 8 -------------

    def _post_with_retry(self, url: str, headers: dict, json_body: dict, stream: bool = False):
        attempt = 0
        while True:
            attempt += 1
            try:
                response = requests.post(
                    url, headers=headers, json=json_body, stream=stream, timeout=self.timeout_s
                )
            except requests.RequestException as exc:
                if attempt >= self.max_retries:
                    raise NeoMundiApiError(f"Network error calling {url} after {attempt} attempts: {exc}") from exc
                time.sleep(10 * attempt)  # linear backoff
                continue

            if response.status_code >= 500:
                if attempt >= self.max_retries:
                    response.raise_for_status()
                time.sleep(10 * attempt)
                continue

            if response.status_code == 429 or "rate_limit" in response.text.lower():
                if attempt >= self.max_retries:
                    response.raise_for_status()
                time.sleep(60)
                continue

            if response.status_code >= 400:
                # Other 4xx: do not retry -- malformed request or invalid key.
                raise NeoMundiApiError(
                    f"{url} returned HTTP {response.status_code}: {response.text[:500]}"
                )

            return response

    # -- step 1 -------------------------------------------------------------

    def _govern_stream(self, prompt: str, arm: ProviderModelArm, provider_api_key: str) -> tuple[str, list[dict]]:
        payload = build_govern_stream_payload(prompt, arm, provider_api_key)
        headers = {
            "X-API-Key": self.neomundi_api_key,
            "Accept": "text/event-stream",
            "Content-Type": "application/json; charset=utf-8",
        }
        response = self._post_with_retry(f"{self.base_url}/v1/govern/stream", headers, payload, stream=True)

        events: list[dict] = []
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            line = line.strip()
            if not line.startswith("data:"):
                continue
            body = line[len("data:"):].strip()
            if not body or body == "[DONE]":
                continue
            try:
                parsed = json.loads(body)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                events.append(parsed)

        response_text = extract_stream_final_text(events) or ""
        return response_text, events

    # -- step 2 -------------------------------------------------------------

    def _govern(self, prompt: str, response_text: str, latency_ms: float | None, token_count: int | None) -> dict:
        raw_metrics = {}
        if token_count is not None:
            raw_metrics["token_count"] = token_count
        if latency_ms is not None:
            raw_metrics["latency_ms"] = round(latency_ms)

        payload = {
            "source_type": "llm",
            "mode": "OBS",
            "llm_prompt": prompt,
            "llm_response": response_text,
            "raw_metrics": raw_metrics,
        }
        headers = {
            "X-API-Key": self.neomundi_api_key,
            "Content-Type": "application/json; charset=utf-8",
        }
        response = self._post_with_retry(f"{self.base_url}/v1/govern", headers, payload)
        return response.json()

    # -- step 3 (optional) ---------------------------------------------------

    def _get_signed_contract(self, request_id: str) -> dict | None:
        headers = {"X-API-Key": self.neomundi_api_key}
        try:
            response = requests.post(
                f"{self.base_url}/v1/rgc/contracts/{request_id}", headers=headers, timeout=self.timeout_s
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            # Per the guide: do not fail the whole observation if step 3 fails.
            return None

    # -- orchestration --------------------------------------------------------

    def measure(
        self,
        prompt: str,
        arm: ProviderModelArm,
        provider_api_key: str | None,
        seed_key: str = "",
    ) -> MeasurementResult:
        if not provider_api_key:
            return MeasurementResult(
                measurement=None,
                latency_ms=None,
                token_count=None,
                rgc_contract=None,
                error=f"No provider API key resolved for arm {arm.arm_id!r}.",
            )
        start = time.monotonic()
        try:
            response_text, events = self._govern_stream(prompt, arm, provider_api_key)
            client_latency_ms = (time.monotonic() - start) * 1000
            latency_ms = extract_stream_latency_ms(events) or client_latency_ms
            token_count = extract_stream_token_count(events)

            govern_response = self._govern(prompt, response_text, latency_ms, token_count)
            measurement = build_measurement_record(govern_response)

            rgc_contract = None
            if self.fetch_signed_contract and measurement.request_id:
                rgc_contract = self._get_signed_contract(measurement.request_id)

            return MeasurementResult(
                measurement=measurement,
                latency_ms=latency_ms,
                token_count=token_count,
                rgc_contract=rgc_contract,
                error=None,
            )
        except Exception as exc:  # noqa: BLE001 -- surfaced as a per-observation error, not a crash
            return MeasurementResult(
                measurement=None,
                latency_ms=None,
                token_count=None,
                rgc_contract=None,
                error=str(exc),
            )
