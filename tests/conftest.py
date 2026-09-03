from __future__ import annotations

from pathlib import Path

import pytest

DATASET_CSV = """prompt_id,prompt,prompt_family,domain
p001,Explain one potential risk of generative AI in a regulated environment.,risk,regulatory
p002,Explain one potential benefit of generative AI in a regulated environment.,benefit,regulatory
p003,Summarize the key obligations of a data controller.,summarization,legal
"""

SINGLE_ARM_CAMPAIGN = """
campaign_id: test_single_arm
dataset: {dataset_path}
providers_models:
  - provider: openai
    model: gpt-4o-2024-11-20
repetitions: 3
output_dir: {output_dir}
notes: "single-arm test campaign"
"""

TWO_MODEL_CAMPAIGN = """
campaign_id: test_two_model
dataset: {dataset_path}
providers_models:
  - provider: openai
    model: gpt-4o-2024-11-20
  - provider: openai
    model: gpt-4o-mini
repetitions: 2
baseline_arm_id: "openai:gpt-4o-2024-11-20"
output_dir: {output_dir}
notes: "two-model test campaign"
"""

MULTI_PROVIDER_CAMPAIGN = """
campaign_id: test_multi_provider
dataset: {dataset_path}
providers_models:
  - provider: openai
    model: gpt-4o-2024-11-20
  - provider: anthropic
    model: claude-sonnet-5
  - provider: mistral
    model: mistral-large
repetitions: 2
baseline_arm_id: "openai:gpt-4o-2024-11-20"
output_dir: {output_dir}
notes: "multi-provider test campaign"
"""


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture
def dataset_path(workspace: Path) -> Path:
    path = workspace / "dataset.csv"
    path.write_text(DATASET_CSV, encoding="utf-8")
    return path


def _write_campaign(workspace: Path, dataset_path: Path, template: str, filename: str) -> Path:
    output_dir = workspace / "outputs"
    content = template.format(dataset_path=str(dataset_path).replace("\\", "/"), output_dir=str(output_dir).replace("\\", "/"))
    path = workspace / filename
    path.write_text(content, encoding="utf-8")
    return path


@pytest.fixture
def single_arm_campaign_path(workspace: Path, dataset_path: Path) -> Path:
    return _write_campaign(workspace, dataset_path, SINGLE_ARM_CAMPAIGN, "single_arm.yaml")


@pytest.fixture
def two_model_campaign_path(workspace: Path, dataset_path: Path) -> Path:
    return _write_campaign(workspace, dataset_path, TWO_MODEL_CAMPAIGN, "two_model.yaml")


@pytest.fixture
def multi_provider_campaign_path(workspace: Path, dataset_path: Path) -> Path:
    return _write_campaign(workspace, dataset_path, MULTI_PROVIDER_CAMPAIGN, "multi_provider.yaml")
