"""Dataset validation: catch problems before a campaign burns API calls on them."""

from __future__ import annotations

from dataclasses import dataclass, field

from periscope.datasets.loader import PromptRecord


@dataclass
class DatasetValidationReport:
    total: int
    duplicate_prompt_ids: list[str] = field(default_factory=list)
    empty_prompts: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.duplicate_prompt_ids and not self.empty_prompts


def validate_dataset(records: list[PromptRecord]) -> DatasetValidationReport:
    seen: dict[str, int] = {}
    duplicates: list[str] = []
    empty: list[str] = []

    for record in records:
        seen[record.prompt_id] = seen.get(record.prompt_id, 0) + 1
        if not record.prompt.strip():
            empty.append(record.prompt_id)

    duplicates = sorted(pid for pid, count in seen.items() if count > 1)

    return DatasetValidationReport(
        total=len(records),
        duplicate_prompt_ids=duplicates,
        empty_prompts=empty,
    )


def require_valid(records: list[PromptRecord]) -> DatasetValidationReport:
    report = validate_dataset(records)
    if not report.is_valid:
        problems = []
        if report.duplicate_prompt_ids:
            problems.append(f"duplicate prompt_id(s): {report.duplicate_prompt_ids}")
        if report.empty_prompts:
            problems.append(f"empty prompt(s) for id(s): {report.empty_prompts}")
        raise ValueError("Dataset validation failed: " + "; ".join(problems))
    return report
