import os
import time
import tempfile
import logging

from pydub import AudioSegment
from dotenv import load_dotenv
from google import genai
from google.genai import types as gtypes
from google.genai.errors import APIError, ClientError
import gradio as gr

try:
    from openai import OpenAI, APIStatusError, APIConnectionError
    OPENAI_SDK_AVAILABLE = True
except ImportError:
    OPENAI_SDK_AVAILABLE = False

# -------------------------
# Logging
# -------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("chatbot")

# -------------------------
# Load Environment
# -------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not GEMINI_API_KEY and not GROQ_API_KEY and not OPENROUTER_API_KEY:
    raise RuntimeError(
        "No API keys found. Set at least one of GEMINI_API_KEY, GROQ_API_KEY, "
        "or OPENROUTER_API_KEY in a .env file next to app.py.\n"
        "  - Gemini (free):      https://aistudio.google.com/apikey\n"
        "  - Groq (free):        https://console.groq.com/keys\n"
        "  - OpenRouter (free):  https://openrouter.ai/keys"
    )

gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
groq_client = (
    OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
    if GROQ_API_KEY and OPENAI_SDK_AVAILABLE else None
)
openrouter_client = (
    OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")
    if OPENROUTER_API_KEY and OPENAI_SDK_AVAILABLE else None
)

if (GROQ_API_KEY or OPENROUTER_API_KEY) and not OPENAI_SDK_AVAILABLE:
    log.warning("GROQ/OPENROUTER key set but the 'openai' package isn't installed — "
                "those providers will be skipped. Run: pip install openai")

# -------------------------
# Provider chain config
# -------------------------
# Each entry: (label, kind, model_name[, client])
#   kind "gemini" uses the google-genai client; kind "openai_compat" uses the openai SDK.
PROVIDER_CHAIN = []
if gemini_client:
    PROVIDER_CHAIN.append(("Gemini 3.1 Pro", "gemini", "gemini-3.1-pro-preview"))
    PROVIDER_CHAIN.append(("Gemini 3.5 Flash", "gemini", "gemini-3.5-flash"))
if groq_client:
    PROVIDER_CHAIN.append(("Groq Llama 3.3 70B", "openai_compat", "llama-3.3-70b-versatile", groq_client))
if openrouter_client:
    PROVIDER_CHAIN.append(("OpenRouter Llama 3.1 8B (free)", "openai_compat", "meta-llama/llama-3.1-8b-instruct:free", openrouter_client))

if not PROVIDER_CHAIN:
    raise RuntimeError(
        "No usable AI provider is configured. Add at least one working API key to .env."
    )

GEMINI_THINKING_CONFIG = gtypes.GenerateContentConfig(
    thinking_config=gtypes.ThinkingConfig(thinking_level="high")
)
GEMINI_THINKING_CONFIG_FLASH = gtypes.GenerateContentConfig(
    thinking_config=gtypes.ThinkingConfig(thinking_level="low")
)

MAX_RETRIES_PER_MODEL = 2
RETRY_BACKOFF_SECONDS = 1.5


def _is_retryable(err: Exception) -> bool:
    """Overload / rate-limit / transient errors we should retry or fail over on."""
    msg = str(err)
    code = getattr(err, "code", None) or getattr(err, "status_code", None)
    if code in (429, 500, 502, 503, 504):
        return True
    lowered = msg.lower()
    return any(s in lowered for s in (
        "unavailable", "resource_exhausted", "overloaded", "rate limit",
        "too many requests", "timeout", "capacity",
    ))


def _stream_gemini(model_name, contents, config):
    last_err = None
    for attempt in range(1, MAX_RETRIES_PER_MODEL + 1):
        try:
            stream = gemini_client.models.generate_content_stream(
                model=model_name, contents=contents, config=config,
            )
            for chunk in stream:
                text = getattr(chunk, "text", None)
                if text:
                    yield text
            return
        except (APIError, ClientError) as e:
            last_err = e
            if _is_retryable(e) and attempt < MAX_RETRIES_PER_MODEL:
                log.warning("Gemini %s attempt %d failed (%s), retrying...", model_name, attempt, e)
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)
                continue
            raise
    if last_err:
        raise last_err


def _stream_openai_compat(client, model_name, messages):
    last_err = None
    for attempt in range(1, MAX_RETRIES_PER_MODEL + 1):
        try:
            stream = client.chat.completions.create(
                model=model_name, messages=messages, stream=True,
            )
            for event in stream:
                delta = event.choices[0].delta.content if event.choices else None
                if delta:
                    yield delta
            return
        except (APIStatusError, APIConnectionError) as e:
            last_err = e
            if _is_retryable(e) and attempt < MAX_RETRIES_PER_MODEL:
                log.warning("%s attempt %d failed (%s), retrying...", model_name, attempt, e)
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)
                continue
            raise
    if last_err:
        raise last_err


def safe_generate_stream(history, latest_user_content):
    """
    Tries each configured provider in order (Gemini Pro -> Gemini Flash -> Groq -> OpenRouter).
    latest_user_content: either a string, or a list of google-genai Parts (for audio input,
    Gemini-only — non-Gemini providers get a text placeholder instead).
    Yields text chunks. Raises RuntimeError only if every provider fails.
    """
    errors = []
    is_multimodal = not isinstance(latest_user_content, str)

    for entry in PROVIDER_CHAIN:
        label, kind = entry[0], entry[1]

        if is_multimodal and kind != "gemini":
            continue  # only Gemini in this app handles raw audio input

        try:
            if kind == "gemini":
                model_name = entry[2]
                config = GEMINI_THINKING_CONFIG if "Pro" in label else GEMINI_THINKING_CONFIG_FLASH
                contents = _build_gemini_contents(history, latest_user_content)
                got_any = False
                for text in _stream_gemini(model_name, contents, config):
                    got_any = True
                    yield text
                if got_any:
                    return
                errors.append(f"{label}: empty response (possibly safety-filtered)")
                continue
            else:
                model_name, client = entry[2], entry[3]
                messages = _build_openai_messages(history, latest_user_content)
                got_any = False
                for text in _stream_openai_compat(client, model_name, messages):
                    got_any = True
                    yield text
                if got_any:
                    return
                errors.append(f"{label}: empty response")
                continue
        except Exception as e:
            log.warning("Provider %s failed: %s", label, e)
            errors.append(f"{label}: {e}")
            continue

    raise RuntimeError(
        "All configured AI providers failed or returned nothing.\n" + "\n".join(f"- {e}" for e in errors)
    )


def _build_gemini_contents(history, latest_user_content):
    """Build a plain conversation transcript + the latest turn (text or multimodal parts)."""
    transcript = _history_to_text(history)
    if isinstance(latest_user_content, str):
        prompt = transcript + f"User: {latest_user_content}\nAI:"
        return prompt
    # multimodal: latest_user_content is a list of Parts (e.g. transcription instruction + audio)
    prefix = transcript + "User (voice message, respond to what they said in the audio):\nAI:"
    return [prefix] + latest_user_content


def _build_openai_messages(history, latest_user_content):
    messages = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["content"]})
    text = latest_user_content if isinstance(latest_user_content, str) else "[voice message]"
    messages.append({"role": "user", "content": text})
    return messages


def _history_to_text(history):
    lines = []
    for msg in history:
        role = "User" if msg["role"] == "user" else "AI"
        lines.append(f"{role}: {msg['content']}")
    return ("\n".join(lines) + "\n") if lines else ""


# -------------------------
# Chat Function (text)
# -------------------------
def chat(message, history):
    history = history or []
    if not message or not message.strip():
        yield history, ""
        return

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": ""})

    try:
        for text in safe_generate_stream(history[:-2], message):
            history[-1]["content"] += text
            yield history, ""
        if not history[-1]["content"]:
            history[-1]["content"] = "⚠️ No response generated — all providers returned empty. Try rephrasing."
            yield history, ""
    except Exception as e:
        log.exception("Chat generation failed")
        history[-1]["content"] = f"❌ {e}"
        yield history, ""


# -------------------------
# Voice Function — sends raw audio straight to Gemini (no separate STT step)
# -------------------------
def voice(audio, history):
    history = history or []

    if audio is None:
        yield history, "No audio captured. Click the mic, speak, then click it again to stop."
        return

    if not gemini_client:
        yield history, "Voice input requires a Gemini API key (used for native audio understanding). Add GEMINI_API_KEY to .env."
        return

    temp_file = None
    try:
        temp_file = os.path.join(tempfile.gettempdir(), f"voice_{int(time.time()*1000)}.ogg")
        try:
            AudioSegment.from_file(audio).export(temp_file, format="ogg")
        except Exception as e:
            yield history, f"Couldn't process the audio file: {e}"
            return

        with open(temp_file, "rb") as f:
            audio_bytes = f.read()

        if len(audio_bytes) < 200:
            yield history, "Recording seems empty — try again and speak right after clicking the mic."
            return

        audio_part = gtypes.Part.from_bytes(data=audio_bytes, mime_type="audio/ogg")
        instruction_part = (
            "The user sent this as a voice message. First transcribe it, then reply "
            "naturally as the assistant, continuing the conversation. Don't repeat the "
            "transcript back verbatim in your reply unless asked."
        )

        history.append({"role": "user", "content": "🎤 (voice message)"})
        history.append({"role": "assistant", "content": ""})

        got_any = False
        for text in safe_generate_stream(history[:-2], [instruction_part, audio_part]):
            got_any = True
            history[-1]["content"] += text
            yield history, "(transcribed automatically by the model)"
        if not got_any:
            history[-1]["content"] = "⚠️ No response generated from the audio."
            yield history, ""

    except Exception as e:
        log.exception("Voice pipeline failed")
        yield history, f"Voice system failure: {e}"
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except OSError:
                pass


# -------------------------
# UI Form Reset
# -------------------------
def reset():
    return [], ""


# -------------------------
# AI Control Matrix UI Layout
# -------------------------
provider_labels = [p[0] for p in PROVIDER_CHAIN]

with gr.Blocks(title="AI Control Matrix") as app:

    with gr.Row(variant="compact"):
        with gr.Column(scale=3):
            gr.HTML("<h2 style='margin:0; padding:5px;'>⚙️ AI Control Matrix</h2>")
        with gr.Column(scale=1, min_width=100):
            clear_btn = gr.Button("Reset Session", variant="stop", size="sm")

    gr.HTML(
        "<div style='background:#e7f1ff;color:#084298;padding:8px 12px;"
        "border-radius:6px;margin:6px 0;font-size:0.85em;'>"
        f"🔗 Active fallback chain: {' → '.join(provider_labels)}"
        "</div>"
    )

    if not gemini_client:
        gr.HTML(
            "<div style='background:#fff3cd;color:#664d03;padding:8px 12px;"
            "border-radius:6px;margin:6px 0;font-size:0.9em;'>"
            "⚠️ No Gemini key set — voice input is disabled (it needs Gemini's audio understanding)."
            "</div>"
        )

    gr.HTML("<hr style='margin: 10px 0;'>")

    with gr.Row():
        with gr.Column(scale=2, variant="panel"):
            gr.Markdown("### 🎤 Audio Ingest Deck")

            mic = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label=None,
                container=False,
                interactive=bool(gemini_client),
            )

            voice_btn = gr.Button("Use Voice", variant="primary", interactive=bool(gemini_client))
            gr.HTML("<br>")

            voice_text = gr.Textbox(
                label="Voice Status",
                placeholder="Awaiting audio capture matrix...",
                interactive=False,
            )

        with gr.Column(scale=3):
            chatbox = gr.Chatbot(
                height=400,
                show_label=False,
            )

            with gr.Row(variant="compact"):
                user_input = gr.Textbox(
                    placeholder="Enter your question...",
                    show_label=False,
                    scale=4,
                    container=False,
                )
                send_btn = gr.Button("Ask", variant="primary", scale=1)

    send_btn.click(chat, inputs=[user_input, chatbox], outputs=[chatbox, user_input])
    user_input.submit(chat, inputs=[user_input, chatbox], outputs=[chatbox, user_input])
    voice_btn.click(voice, inputs=[mic, chatbox], outputs=[chatbox, voice_text])
    clear_btn.click(reset, outputs=[chatbox, voice_text])

if __name__ == "__main__":
    app.launch()
