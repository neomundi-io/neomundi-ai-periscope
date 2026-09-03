"""Expand a dataset x arms x repetitions campaign into a flat execution plan."""

from __future__ import annotations

from dataclasses import dataclass

from periscope.campaign.configuration import CampaignConfig
from periscope.datasets.loader import PromptRecord
from periscope.providers.adapter import ProviderModelArm


@dataclass(frozen=True)
class ExecutionUnit:
    prompt: PromptRecord
    arm: ProviderModelArm
    repetition_index: int
    planned_repetitions: int


def build_execution_plan(config: CampaignConfig, prompts: list[PromptRecord]) -> list[ExecutionUnit]:
    """1 dataset x N arms x N repetitions, without duplicating the engine
    per provider or per model."""
    plan: list[ExecutionUnit] = []
    for prompt in prompts:
        for arm in config.arms:
            for repetition_index in range(1, config.repetitions + 1):
                plan.append(
                    ExecutionUnit(
                        prompt=prompt,
                        arm=arm,
                        repetition_index=repetition_index,
                        planned_repetitions=config.repetitions,
                    )
                )
    return plan
