from pathlib import Path
import os

import requests
import yaml


CONFIG_FILE = "config.yaml"
API_URL = "https://api.neomundi.io/v1/govern/stream"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_prompts(prompt_file):
    path = Path(prompt_file)

    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

    content = path.read_text(encoding="utf-8")

    prompts = [
        prompt.strip()
        for prompt in content.split("---")
        if prompt.strip()
    ]

    if not prompts:
        raise ValueError("No prompts found in the selected prompt file.")

    return prompts


def call_controltower(prompt, config, controltower_key, provider_key):
    payload = {
        "prompt": prompt,
        "provider": config["provider"],
        "provider_api_key": provider_key,
        "model": config["model"],
    }

    if config.get("temperature") is not None:
        payload["temperature"] = config["temperature"]

    if config.get("max_tokens") is not None:
        payload["max_tokens"] = config["max_tokens"]

    headers = {
        "X-API-Key": controltower_key,
        "Content-Type": "application/json",
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        stream=True,
        timeout=300,
    )

    response.raise_for_status()

    return response.text


def main():
    config = load_config()

    controltower_key = os.getenv("CONTROLTOWER_API_KEY")
    provider_key = os.getenv("PROVIDER_API_KEY")

    if not controltower_key:
        raise ValueError(
            "Missing CONTROLTOWER_API_KEY. "
            "Launch AI Periscope with RUN_PERISCOPE.ps1."
        )

    if not provider_key:
        raise ValueError(
            "Missing PROVIDER_API_KEY. "
            "Add the provider key in RUN_PERISCOPE.ps1."
        )

    required_fields = [
        "provider",
        "model",
        "prompt_file",
        "runs_per_prompt",
    ]

    for field in required_fields:
        if config.get(field) in (None, ""):
            raise ValueError(
                f"Missing required field in config.yaml: {field}"
            )

    prompts = load_prompts(config["prompt_file"])

    runs_per_prompt = int(config["runs_per_prompt"])

    if runs_per_prompt < 1:
        raise ValueError("runs_per_prompt must be at least 1.")

    total_requests = len(prompts) * runs_per_prompt

    print("")
    print("NeoMundi AI Periscope")
    print("---------------------")
    print(f"Provider        : {config['provider']}")
    print(f"Model           : {config['model']}")
    print(f"Prompt file     : {config['prompt_file']}")
    print(f"Prompts         : {len(prompts)}")
    print(f"Runs per prompt : {runs_per_prompt}")
    print(f"Total requests  : {total_requests}")
    print("")

    current = 0

    for prompt_index, prompt in enumerate(prompts, start=1):

        for run_index in range(1, runs_per_prompt + 1):

            current += 1

            print(
                f"[{current}/{total_requests}] "
                f"Prompt {prompt_index} / Run {run_index}"
            )

            call_controltower(
                prompt=prompt,
                config=config,
                controltower_key=controltower_key,
                provider_key=provider_key,
            )

    print("")
    print("Campaign complete.")


if __name__ == "__main__":
    main()
