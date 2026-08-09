from pathlib import Path
import os

import requests
import yaml
from dotenv import load_dotenv


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
    load_dotenv()

    config = load_config()

    controltower_key = os.getenv("CONTROLTOWER_API_KEY")
    provider_key = os.getenv("PROVIDER_API_KEY")

    if not controltower_key:
        raise ValueError("Missing CONTROLTOWER_API_KEY in .env")

    if not provider_key:
        raise ValueError("Missing PROVIDER_API_KEY in .env")

    prompts = load_prompts(config["prompt_file"])
    runs_per_prompt = int(config["runs_per_prompt"])

    total_requests = len(prompts) * runs_per_prompt

    print("NeoMundi AI Periscope")
    print("---------------------")
    print(f"Provider: {config['provider']}")
    print(f"Model: {config['model']}")
    print(f"Prompts: {len(prompts)}")
    print(f"Runs per prompt: {runs_per_prompt}")
    print(f"Total requests: {total_requests}")
    print()

    current = 0

    for prompt_index, prompt in enumerate(prompts, start=1):
        for run_index in range(1, runs_per_prompt + 1):
            current += 1

            print(
                f"[{current}/{total_requests}] "
                f"Prompt {prompt_index} / Run {run_index}"
            )

            call_controltower(
                prompt,
                config,
                controltower_key,
                provider_key,
            )

    print()
    print("Campaign complete.")


if __name__ == "__main__":
    main()
