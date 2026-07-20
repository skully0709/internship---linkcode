# AI Chatbot with Voice Input (Multi-Provider)

A Gradio chatbot backed by **three independent AI providers with automatic fallback**, so "too many requests" / rate-limit / overload errors on one provider no longer break the app. Supports text and voice (voice uses Gemini's native audio understanding — no separate speech-recognition service).

## Why multi-provider?

If you were hitting "too many users are requesting" errors, that's a single provider (Gemini) rate-limiting you. This version tries, in order:

1. **Gemini 3.1 Pro** (best quality, "thinking" enabled)
2. **Gemini 3.5 Flash** (same key, faster/cheaper, used as first fallback)
3. **Groq — Llama 3.3 70B** (separate free provider, extremely fast)
4. **OpenRouter — Llama 3.1 8B (free)** (separate free provider, final fallback)

Only providers with a key set in `.env` are used — you can run with just one key, but adding more makes the app noticeably more resilient. Each hop only triggers on a genuinely retryable failure (rate limit, overload, timeout) — errors like a bad request or invalid key surface immediately instead of being silently retried.

## Setup

1. `cd` into this folder.
2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   ```
   Activate it:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Install ffmpeg (required for voice input's audio conversion step, not a pip package):
   - Windows: `winget install ffmpeg` (restart terminal after)
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`
5. Get your API key(s) — all free, no credit card required for any of them:
   - **Gemini** (needed for voice input): https://aistudio.google.com/apikey
   - **Groq**: https://console.groq.com/keys
   - **OpenRouter**: https://openrouter.ai/keys
6. Copy `.env.example` to `.env` and paste in whichever keys you have. You don't need all three, but Gemini is required if you want voice input.

**Never commit your real `.env` file or share it** — each key grants access to that provider's quota/billing. `.gitignore` already excludes it.

## Run

```
python app.py
```

Open the local URL Gradio prints (e.g. `http://127.0.0.1:7860`). The top of the page shows which providers are active and in what fallback order.

- **Text**: type and press Enter or click **Ask**.
- **Voice**: click the mic, speak, click the mic again to stop, then click **Use Voice**. The raw audio is sent straight to Gemini, which transcribes and replies in one step — no separate speech-recognition service, so it's not subject to that service's own rate limits. (Requires a Gemini key; greyed out otherwise.)
- **Reset Session**: clears the chat.

## Troubleshooting

- **"No API keys found"**: copy `.env.example` to `.env` and add at least one real key.
- **Chat shows "All configured AI providers failed"**: every provider you configured is down or rate-limited at the same time — wait a bit, or add another provider's key for more redundancy. The error message lists exactly what each provider returned.
- **"ffmpeg not found"** / voice errors about processing audio: install ffmpeg (step 4) and restart the app.
- **Nothing recorded / timer resets to 0**: some browsers (e.g. Brave) block mic access via privacy shields — turn Shields off for the page, or try Chrome.
- **Voice button greyed out**: no `GEMINI_API_KEY` set — voice needs Gemini specifically for audio understanding.
- **Empty/blocked responses**: safety filters may have blocked a reply on that provider; the app will still try the next one in the chain.

## Notes on the free tiers

Free tiers change over time and are rate-limited by nature — that's expected, and is exactly why this app spreads requests across providers instead of relying on one. If you outgrow all three free tiers, the cheapest next step is usually adding a paid key for one of them (Gemini, Groq, and OpenRouter all support pay-as-you-go).

## Security note

API keys are read only from a local `.env` file, never hardcoded in source. Rotate any key immediately at its provider's dashboard if it's ever been shared, committed to git, or exposed in a file you sent to someone else — including inside a zipped project folder.
