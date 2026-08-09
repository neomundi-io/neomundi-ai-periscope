from pathlib import Path
import os
import yaml
import requests


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


def main():
    config = load_config()

    print("NeoMundi AI Periscope")
    print("---------------------")
    print(f"Provider: {config.get('provider')}")
    print(f"Model: {config.get('model')}")
    print(f"Prompt file: {config.get('prompt_file')}")
    print(f"Runs per prompt: {config.get('runs_per_prompt')}")


if __name__ == "__main__":
    main()
