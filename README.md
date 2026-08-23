# AI: Scaffolding a Robust API Integration

## AI Tool Used
Claude (Anthropic), used as the contextual-prompting target for this exercise.

## Objective
Use a single, comprehensive **Contextual Prompt** to refactor `sentiment_analyzer.py` so it:
1. Securely reads an API key from the `TEXT_PROCESSING_API_KEY` environment variable and sends it as a standard `Authorization: Bearer <key>` header.
2. Explicitly catches `requests.exceptions.Timeout` and `requests.exceptions.ConnectionError` as their own exception handlers (each with a distinct, informative `sys.stderr` message), ordered before the existing, broader `HTTPError` / `RequestException` handlers.

## Files in This Folder
| File | Description |
|---|---|
| `sentiment_analyzer_initial.py` | The original script, exactly as provided in the assignment. |
| `sentiment_analyzer_refactored.py` | The AI-refactored script, produced from the contextual prompt below, pointed at the real `https://api.text-processing.com` endpoint. |
| `mock_api_server.py` | A small local HTTP server used only to demonstrate the refactored script end-to-end in a sandboxed environment where the real API host is not reachable. Not part of the production tool. |

## The Contextual Prompt

> I'm working on a Python CLI tool called sentiment_analyzer.py that calls a public sentiment-analysis API. Here is the full current code:
>
> ```python
> #!/usr/bin/python3
> """
> Sentiment Analysis Tool
> Analyzes the sentiment of a given sentence using a public API.
> """
> import requests
> import sys
>
> def analyze_sentiment(text):
>     """
>     Analyzes the sentiment of the given text using the Text Processing API.
>     Args:
>         text (str): The sentence to analyze
>     Returns:
>         str: The sentiment label (positive, negative, or neutral)
>     """
>     url = "https://api.text-processing.com/api/sentiment/"
>     payload = {"text": text}
>     try:
>         response = requests.post(url, data=payload)
>         response.raise_for_status()
>         data = response.json()
>         label = data.get('label', 'neutral')
>         if label == 'pos':
>             return 'positive'
>         elif label == 'neg':
>             return 'negative'
>         else:
>             return 'neutral'
>     except requests.exceptions.HTTPError as e:
>         print(f"HTTP Error: {e}", file=sys.stderr)
>         return None
>     except requests.exceptions.RequestException as e:
>         print(f"Request failed: {e}", file=sys.stderr)
>         return None
>     except (KeyError, ValueError) as e:
>         print(f"Invalid response format: {e}", file=sys.stderr)
>         return None
>
> if __name__ == "__main__":
>     if len(sys.argv) < 2:
>         print("Usage: ./sentiment_analyzer.py <sentence>")
>         sys.exit(1)
>     sentence = " ".join(sys.argv[1:])
>     result = analyze_sentiment(sentence)
>     if result:
>         print(result)
>     else:
>         sys.exit(1)
> ```
>
> Using this exact code as your starting point, please refactor the `analyze_sentiment` function so it securely reads an API key from the environment variable `TEXT_PROCESSING_API_KEY` (import the `os` module) and sends it in the request headers as `"Authorization: Bearer <key>"`. Also refine the existing try/except block by explicitly adding `requests.exceptions.Timeout` and `requests.exceptions.ConnectionError` as their own except clauses, each printing a distinct, informative error message to `sys.stderr`, placed before the existing broader `requests.exceptions.HTTPError` and `requests.exceptions.RequestException` handlers. Keep the rest of the script's structure and behavior (including the `__main__` block) unchanged, and return the complete, updated file.

## Summary of Changes
- Added `import os` and a `TEXT_PROCESSING_API_KEY` read via `os.environ.get(...)`, with a fail-fast, clear error message if it's unset — the key is never hardcoded.
- Added `headers = {"Authorization": f"Bearer {api_key}"}` and passed it into `requests.post(...)`, along with a `timeout=10` safety net.
- Added explicit `except requests.exceptions.Timeout` and `except requests.exceptions.ConnectionError` clauses, each with a distinct message, both placed **before** the pre-existing `HTTPError` / `RequestException` handlers (required, since both are subclasses of `RequestException` and Python evaluates `except` clauses in order).
- All other structure, the `__main__` block, and the `KeyError`/`ValueError` handling were left unchanged, per the prompt's instructions.

## Verification
Running the refactored script with `TEXT_PROCESSING_API_KEY` set correctly returns `positive` / `negative` / `neutral` labels for sample sentences, and running it with the variable unset now returns a clear `Configuration Error` message and exits with status 1, instead of silently sending an unauthenticated request. Full execution details and screenshots are included in the accompanying submission document.
