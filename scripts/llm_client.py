#!/usr/bin/env python3
import json
import os
import urllib.error
import urllib.request


DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o-mini"


def require_env(name):
    value = os.getenv(name)
    if not value:
        raise SystemExit(
            f"{name} is not set. Export it before running LLM mode."
        )
    return value


def chat_completion(prompt):
    api_key = require_env("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    model = os.getenv("LLM_MODEL", DEFAULT_MODEL)

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a senior Java Spring Boot unit testing assistant. "
                    "Return practical, test-focused suggestions only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    request = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            response_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise SystemExit(
            f"LLM request failed with HTTP {error.code}: {error_body}"
        ) from error
    except urllib.error.URLError as error:
        raise SystemExit(f"LLM request failed: {error}") from error

    data = json.loads(response_body)
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as error:
        raise SystemExit(
            f"LLM response did not contain a chat completion: {response_body}"
        ) from error
