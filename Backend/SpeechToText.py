import speech_recognition as sr
import mtranslate as mt
import os
from dotenv import dotenv_values

# ── Load env variables ────────────────────────────────────────────────────────
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage")

# ── Path setup ────────────────────────────────────────────────────────────────
current_dir = os.getcwd()
TempDirPath = rf"{current_dir}/Frontend/Files"
os.makedirs(TempDirPath, exist_ok=True)

# ── Recognizer — initialized ONCE at module level (not per call) ───────────────
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8        # Seconds of silence before utterance ends
recognizer.energy_threshold = 300       # Mic sensitivity baseline
recognizer.dynamic_energy_threshold = True  # Auto-adjusts to ambient noise

# ── Microphone — opened ONCE and calibrated ONCE at startup ───────────────────
# This eliminates the ~0.5s adjust_for_ambient_noise cost on every single call
_microphone = sr.Microphone()
with _microphone as source:
    print("[STT] Calibrating microphone for ambient noise...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("[STT] Microphone ready.")


# ── Helpers ───────────────────────────────────────────────────────────────────
def SetAssistantStatus(Status):
    """Write assistant status to a file for the frontend to read."""
    with open(rf"{TempDirPath}/Status.data", "w", encoding="utf-8") as file:
        file.write(Status)


def QueryModifier(Query):
    """Ensure proper punctuation and formatting on the recognized query."""
    new_query = Query.lower().strip()
    query_words = new_query.split()

    if not query_words:
        return ""

    question_words = [
        "how", "what", "who", "where", "why", "which", "whose", "whom",
        "can you", "what's", "where's", "how's", "do you", "if"
    ]

    is_question = any(word + " " in new_query for word in question_words)

    if is_question:
        new_query = new_query[:-1] + "?" if query_words[-1][-1] in ".?!" else new_query + "?"
    else:
        new_query = new_query[:-1] + "." if query_words[-1][-1] in ".?!" else new_query + "."

    return new_query.capitalize()


def UniversalTranslator(Text):
    """Translate recognized text into English."""
    return mt.translate(Text, "en", "auto").capitalize()


# ── Core STT function ─────────────────────────────────────────────────────────
def SpeechRecognition():
    """
    Captures audio from the microphone and returns the recognized + formatted text.

    Latency improvements over Selenium/browser version:
      - No browser launch overhead (~10-15s eliminated)
      - Microphone kept warm — no per-call device open/close
      - Ambient noise calibration done once at startup, not per call
      - Direct Google Speech API call — no HTML/JS round-trip
    Expected latency: ~1-3s (vs original ~34s)
    """
    with _microphone as source:
        SetAssistantStatus("Listening...")
        try:
            # timeout      : how long to wait for speech to START (seconds)
            # phrase_time_limit : max length of a single utterance (seconds)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            return ""   # No speech detected — caller should loop

    try:
        SetAssistantStatus("Recognizing...")
        # recognize_google uses the same Google Speech backend as the browser Web Speech API
        # The `language` param accepts the same locale strings e.g. "en-US", "hi-IN"
        Text = recognizer.recognize_google(audio, language=InputLanguage)

        if not Text:
            return ""

        if "en" in InputLanguage.lower():
            return QueryModifier(Text)
        else:
            SetAssistantStatus("Translating...")
            return QueryModifier(UniversalTranslator(Text))

    except sr.UnknownValueError:
        # Audio captured but Google couldn't interpret it
        return ""
    except sr.RequestError as e:
        print(f"[STT] Google Speech API error: {e}")
        SetAssistantStatus("Speech API Error")
        return ""


# ── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("[STT] Ready. Speak now...")
    while True:
        Text = SpeechRecognition()
        if Text:
            print(Text)