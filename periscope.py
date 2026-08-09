from pathlib import Path
from datetime import datetime, timezone
import csv
import json
import os

import requests
import yaml


CONFIG_FILE = "config.yaml"
API_URL = "https://api.neomundi.io/v1/govern/stream"
RESULTS_DIR = Path("results")


# ============================================================
# CONFIG
# ============================================================

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError("config.yaml is empty or invalid.")

    return config


# ============================================================
# PROMPTS
# ============================================================

def load_prompts(prompt_file):
    path = Path(prompt_file)

    if not path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_file}"
        )

    content = path.read_text(encoding="utf-8")

    prompts = [
        prompt.strip()
        for prompt in content.split("---")
        if prompt.strip()
    ]

    if not prompts:
        raise ValueError(
            "No prompts found in the selected prompt file."
        )

    return prompts


# ============================================================
# SSE / JSON PARSING
# ============================================================

def parse_sse_response(response):
    """
    Reads the ControlTower SSE stream.

    Keeps:
    - the complete raw stream;
    - every JSON object found in SSE `data:` events.

    No measurement value is invented.
    """

    raw_lines = []
    events = []

    for line in response.iter_lines(decode_unicode=True):

        if line is None:
            continue

        line = line.strip()

        if not line:
            continue

        raw_lines.append(line)

        if line.startswith("data:"):
            payload = line[5:].strip()

            if not payload:
                continue

            if payload == "[DONE]":
                continue

            try:
                parsed = json.loads(payload)

                if isinstance(parsed, dict):
                    events.append(parsed)

            except json.JSONDecodeError:
                pass

    return {
        "raw_stream": "\n".join(raw_lines),
        "events": events,
    }


# ============================================================
# FIND VALUES INSIDE CONTROLTOWER EVENTS
# ============================================================

def find_value(obj, possible_keys):
    """
    Recursively searches a JSON structure for the first
    value matching one of the requested keys.
    """

    if isinstance(obj, dict):

        for key in possible_keys:
            if key in obj and obj[key] not in (None, ""):
                return obj[key]

        for value in obj.values():
            found = find_value(value, possible_keys)

            if found not in (None, ""):
                return found

    elif isinstance(obj, list):

        for item in obj:
            found = find_value(item, possible_keys)

            if found not in (None, ""):
                return found

    return None


def extract_measurement_fields(events):
    """
    Extracts measurement fields only when they are actually
    present in the ControlTower response.

    The raw events remain preserved in all cases.
    """

    return {
        "stability_score": find_value(
            events,
            [
                "stability_score",
                "stability",
                "g_final",
                "g_score",
            ],
        ),

        "delta_g": find_value(
            events,
            [
                "delta_g",
                "deltaG",
                "g_delta",
            ],
        ),

        "decision": find_value(
            events,
            [
                "decision",
                "observation_class",
                "classification",
            ],
        ),

        "latency_ms": find_value(
            events,
            [
                "latency_ms",
                "latency",
                "response_latency_ms",
            ],
        ),

        "token_count": find_value(
            events,
            [
                "token_count",
                "total_tokens",
                "tokens",
                "output_tokens",
            ],
        ),
    }


# ============================================================
# CONTROLTOWER CALL
# ============================================================

def call_controltower(
    prompt,
    config,
    controltower_key,
    provider_key,
):

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

    parsed = parse_sse_response(response)

    return {
        "http_status": response.status_code,
        "raw_stream": parsed["raw_stream"],
        "events": parsed["events"],
    }


# ============================================================
# RESULTS FOLDER
# ============================================================

def create_campaign_folder():
    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S")

    campaign_dir = (
        RESULTS_DIR / f"campaign_{timestamp}"
    )

    campaign_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return campaign_dir


# ============================================================
# SAVE JSON
# ============================================================

def save_json(results, path):
    path.write_text(
        json.dumps(
            results,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


# ============================================================
# SAVE CSV
# ============================================================

def save_csv(results, path):

    fields = [
        "prompt_index",
        "run_index",
        "provider",
        "model",
        "prompt",
        "timestamp_utc",
        "http_status",
        "stability_score",
        "delta_g",
        "decision",
        "latency_ms",
        "token_count",
        "error",
        "raw_stream",
        "events",
    ]

    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fields,
        )

        writer.writeheader()

        for result in results:

            row = result.copy()

            row["events"] = json.dumps(
                row.get("events", []),
                ensure_ascii=False,
            )

            writer.writerow(
                {
                    field: row.get(field, "")
                    for field in fields
                }
            )


# ============================================================
# SAVE CAMPAIGN
# ============================================================

def save_campaign(
    results,
    json_path,
    csv_path,
):

    save_json(results, json_path)
    save_csv(results, csv_path)


# ============================================================
# MAIN
# ============================================================

def main():

    config = load_config()

    controltower_key = os.getenv(
        "CONTROLTOWER_API_KEY"
    )

    provider_key = os.getenv(
        "PROVIDER_API_KEY"
    )

    if not controltower_key:
        raise ValueError(
            "Missing CONTROLTOWER_API_KEY. "
            "Launch AI Periscope with RUN_PERISCOPE.ps1."
        )

    if not provider_key:
        raise ValueError(
            "Missing PROVIDER_API_KEY. "
            "Add your provider API key in RUN_PERISCOPE.ps1."
        )


    # ========================================================
    # REQUIRED CONFIG
    # ========================================================

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


    # ========================================================
    # LOAD CAMPAIGN
    # ========================================================

    prompts = load_prompts(
        config["prompt_file"]
    )

    runs_per_prompt = int(
        config["runs_per_prompt"]
    )

    if runs_per_prompt < 1:
        raise ValueError(
            "runs_per_prompt must be at least 1."
        )

    total_requests = (
        len(prompts)
        * runs_per_prompt
    )


    # ========================================================
    # CREATE RESULTS FOLDER
    # ========================================================

    campaign_dir = create_campaign_folder()

    json_path = (
        campaign_dir
        / "campaign_results.json"
    )

    csv_path = (
        campaign_dir
        / "campaign_results.csv"
    )


    # ========================================================
    # CAMPAIGN SUMMARY
    # ========================================================

    print("")
    print("NeoMundi AI Periscope")
    print("---------------------")
    print(
        f"Provider        : "
        f"{config['provider']}"
    )
    print(
        f"Model           : "
        f"{config['model']}"
    )
    print(
        f"Prompt file     : "
        f"{config['prompt_file']}"
    )
    print(
        f"Prompts         : "
        f"{len(prompts)}"
    )
    print(
        f"Runs per prompt : "
        f"{runs_per_prompt}"
    )
    print(
        f"Total requests  : "
        f"{total_requests}"
    )
    print(
        f"Results folder  : "
        f"{campaign_dir}"
    )
    print("")


    # ========================================================
    # RUN CAMPAIGN
    # ========================================================

    results = []

    current = 0

    for prompt_index, prompt in enumerate(
        prompts,
        start=1,
    ):

        for run_index in range(
            1,
            runs_per_prompt + 1,
        ):

            current += 1

            print(
                f"[{current}/{total_requests}] "
                f"Prompt {prompt_index} "
                f"/ Run {run_index}"
            )

            timestamp_utc = datetime.now(
                timezone.utc
            ).isoformat()

            observation = {
                "prompt_index": prompt_index,
                "run_index": run_index,
                "provider": config["provider"],
                "model": config["model"],
                "prompt": prompt,
                "timestamp_utc": timestamp_utc,
                "http_status": None,
                "stability_score": None,
                "delta_g": None,
                "decision": None,
                "latency_ms": None,
                "token_count": None,
                "error": "",
                "raw_stream": "",
                "events": [],
            }

            try:

                response_data = call_controltower(
                    prompt=prompt,
                    config=config,
                    controltower_key=controltower_key,
                    provider_key=provider_key,
                )

                observation["http_status"] = (
                    response_data["http_status"]
                )

                observation["raw_stream"] = (
                    response_data["raw_stream"]
                )

                observation["events"] = (
                    response_data["events"]
                )

                measurements = (
                    extract_measurement_fields(
                        response_data["events"]
                    )
                )

                observation.update(
                    measurements
                )

            except Exception as exc:

                observation["error"] = str(exc)

                results.append(observation)

                save_campaign(
                    results,
                    json_path,
                    csv_path,
                )

                print("")
                print(
                    "ERROR during request:"
                )
                print(str(exc))
                print("")
                print(
                    "Partial campaign results "
                    "were saved."
                )

                raise


            results.append(observation)


            # Save after EACH observation.
            # If the campaign stops later,
            # completed observations remain available.

            save_campaign(
                results,
                json_path,
                csv_path,
            )


    # ========================================================
    # COMPLETE
    # ========================================================

    print("")
    print("Campaign complete.")
    print("")
    print(
        f"JSON results : {json_path}"
    )
    print(
        f"CSV results  : {csv_path}"
    )
    print("")


if __name__ == "__main__":
    main()
