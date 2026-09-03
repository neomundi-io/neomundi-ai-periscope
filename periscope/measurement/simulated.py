"""A deterministic, offline stand-in for the real NeoMundi client.

Used for:
- automated tests, so the test suite never depends on network access or live
  API keys;
- local demos of the campaign engine and reports before a user has NeoMundi /
  provider credentials.

Every record produced here is marked `synthetic: true` in its raw payload,
following the same convention the NeoMundi Metric Contract uses for its own
illustrative examples. A simulated campaign's canonical dataset and reports
must never be presented as real measurements -- `campaign/runner.py` and the
report renderers propagate this flag into the campaign manifest.
"""

from __future__ import annotations

import hashlib
import random

from periscope.measurement.client import MeasurementResult
from periscope.measurement.contracts import (
    MeasurementRecord,
    ObservedSignal,
    SignalStatus,
)
from periscope.providers.adapter import ProviderModelArm

SIMULATED_SCHEMA_VERSION = "0.2.0"
SIMULATED_MEASUREMENT_VERSION = "sim-0.1.0"
SIMULATED_NORMALIZER_VERSION = "sim-0.1.0"


def _seeded_random(seed_key: str) -> random.Random:
    digest = hashlib.sha256(seed_key.encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


class SimulatedMeasurementClient:
    """Deterministic per (prompt, arm, repetition) via `seed_key`.

    `partial_rate` controls how often a signal comes back as
    not_measured/insufficient_coverage instead of measured, so tests and
    demos can exercise Periscope's handling of partial NeoMundi measurements
    without needing a live partial-coverage example from NeoMundi.
    """

    def __init__(self, partial_rate: float = 0.0, flag_rate: float = 0.1) -> None:
        self.partial_rate = partial_rate
        self.flag_rate = flag_rate

    def measure(
        self,
        prompt: str,
        arm: ProviderModelArm,
        provider_api_key: str | None,
        seed_key: str,
    ) -> MeasurementResult:
        rng = _seeded_random(seed_key)

        # A per-arm bias so different (provider, model) arms are
        # distinguishable in comparisons/benchmarks, not just noisy.
        arm_bias = _seeded_random(arm.arm_id).uniform(-0.08, 0.08)

        signals: dict[str, ObservedSignal] = {}
        for name, base, spread in (
            ("stability_score", 0.85, 0.12),
            ("coherence_score", 0.90, 0.10),
            ("factual_hallucination_score", 0.05, 0.08),
            ("semantic_instability_score", 0.08, 0.10),
            ("semantic_risk", 0.04, 0.06),
            ("confidence", 0.88, 0.10),
        ):
            if rng.random() < self.partial_rate:
                status = rng.choice([SignalStatus.NOT_MEASURED, SignalStatus.INSUFFICIENT_COVERAGE])
                signals[name] = ObservedSignal(name=name, value=None, status=status)
                continue
            value = base + arm_bias + rng.uniform(-spread, spread)
            value = max(0.0, min(1.0, value))
            signals[name] = ObservedSignal(name=name, value=round(value, 6), status=SignalStatus.MEASURED)

        any_partial = any(s.status != SignalStatus.MEASURED for s in signals.values())
        measurement_status = "partial" if any_partial else "complete"
        measurement_coverage = round(
            sum(1 for s in signals.values() if s.status == SignalStatus.MEASURED) / len(signals), 4
        )

        flagged = rng.random() < self.flag_rate
        observation_class = "flagged" if flagged else "within_bounds"
        decision = "FLAG" if flagged else "ALLOW"

        latency_ms = round(max(50.0, rng.gauss(650, 180)), 1)
        token_count = max(1, int(rng.gauss(120, 40)))

        request_id = "sim_" + hashlib.sha256(seed_key.encode("utf-8")).hexdigest()[:24]

        measurement = MeasurementRecord(
            request_id=request_id,
            schema_version=SIMULATED_SCHEMA_VERSION,
            measurement_version=SIMULATED_MEASUREMENT_VERSION,
            normalizer_version=SIMULATED_NORMALIZER_VERSION,
            measurement_status=measurement_status,
            measurement_coverage=measurement_coverage,
            observation_class=observation_class,
            decision=decision,
            signals=signals,
            raw={"synthetic": True, "seed_key": seed_key},
        )

        return MeasurementResult(
            measurement=measurement,
            latency_ms=latency_ms,
            token_count=token_count,
            rgc_contract=None,
            error=None,
        )
