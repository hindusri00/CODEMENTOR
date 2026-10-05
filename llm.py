"""LLM layer. Pick a provider with LLM_PROVIDER in .env.

Free options: gemini, groq, openrouter, ollama (local). Paid: anthropic.
All except anthropic use the OpenAI-compatible API, so one code path covers them.
"""
import json
import os
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, build_user_prompt

load_dotenv()

# name: (base_url, api-key env var, default model)
PROVIDERS = {
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai/",
               "GEMINI_API_KEY", "gemini-2.5-flash"),
    "groq": ("https://api.groq.com/openai/v1",
             "GROQ_API_KEY", "openai/gpt-oss-120b"),
    "openrouter": ("https://openrouter.ai/api/v1",
                   "OPENROUTER_API_KEY", ""),  # pick a ':free' model yourself
    "ollama": ("http://localhost:11434/v1", None, "llama3.1"),
    "anthropic": (None, "ANTHROPIC_API_KEY", "claude-sonnet-5-5"),
}

PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()


def _extract_json(text: str) -> dict:
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Model did not return JSON. Try again or use a stronger model.")
    return json.loads(text[start:end + 1])


def _complete(system: str, user: str) -> str:
    if PROVIDER not in PROVIDERS:
        raise ValueError(f"Unknown LLM_PROVIDER '{PROVIDER}'. Use one of: {', '.join(PROVIDERS)}")
    base_url, key_env, default_model = PROVIDERS[PROVIDER]
    model = os.getenv("CODE_MENTOR_MODEL", default_model)
    if not model:
        raise ValueError(f"Set CODE_MENTOR_MODEL in .env for provider '{PROVIDER}'.")
    api_key = os.getenv(key_env) if key_env else "ollama"
    if not api_key:
        raise ValueError(f"Missing {key_env} in your .env file.")

    if PROVIDER == "anthropic":
        import anthropic
        resp = anthropic.Anthropic(api_key=api_key).messages.create(
            model=model, max_tokens=1500, system=system,
            messages=[{"role": "user", "content": user}])
        return resp.content[0].text

    from openai import OpenAI
    resp = OpenAI(base_url=base_url, api_key=api_key).chat.completions.create(
        model=model, max_tokens=1500, temperature=0.3,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}])
    return resp.choices[0].message.content


def explain(code: str, static_text: str, notes: str, hint_level: int) -> dict:
    user = build_user_prompt(code, static_text, notes, hint_level)
    text = _complete(SYSTEM_PROMPT, user)
    try:
        return _extract_json(text)
    except (ValueError, json.JSONDecodeError):
        # Smaller free models sometimes add chatter or break JSON: retry once.
        retry = user + "\n\nReturn ONLY the JSON object. No other text."
        return _extract_json(_complete(SYSTEM_PROMPT, retry))
