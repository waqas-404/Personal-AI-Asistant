# import speech_recognition as sr
# import mtranslate as mt
# import os
# from dotenv import dotenv_values

# # ── Load env variables ────────────────────────────────────────────────────────
# env_vars = dotenv_values(".env")
# InputLanguage = env_vars.get("InputLanguage")

# # ── Path setup ────────────────────────────────────────────────────────────────
# current_dir = os.getcwd()
# TempDirPath = rf"{current_dir}/Frontend/Files"
# os.makedirs(TempDirPath, exist_ok=True)

# # ── Recognizer — initialized ONCE at module level (not per call) ───────────────
# recognizer = sr.Recognizer()
# recognizer.pause_threshold = 0.8        # Seconds of silence before utterance ends
# recognizer.energy_threshold = 300       # Mic sensitivity baseline
# recognizer.dynamic_energy_threshold = True  # Auto-adjusts to ambient noise

# # ── Microphone — opened ONCE and calibrated ONCE at startup ───────────────────
# # This eliminates the ~0.5s adjust_for_ambient_noise cost on every single call
# _microphone = sr.Microphone()
# with _microphone as source:
#     print("[STT] Calibrating microphone for ambient noise...")
#     recognizer.adjust_for_ambient_noise(source, duration=1)
#     print("[STT] Microphone ready.")


# # ── Helpers ───────────────────────────────────────────────────────────────────
# def SetAssistantStatus(Status):
#     """Write assistant status to a file for the frontend to read."""
#     with open(rf"{TempDirPath}/Status.data", "w", encoding="utf-8") as file:
#         file.write(Status)


# def QueryModifier(Query):
#     """Ensure proper punctuation and formatting on the recognized query."""
#     new_query = Query.lower().strip()
#     query_words = new_query.split()

#     if not query_words:
#         return ""

#     question_words = [
#         "how", "what", "who", "where", "why", "which", "whose", "whom",
#         "can you", "what's", "where's", "how's", "do you", "if"
#     ]

#     is_question = any(word + " " in new_query for word in question_words)

#     if is_question:
#         new_query = new_query[:-1] + "?" if query_words[-1][-1] in ".?!" else new_query + "?"
#     else:
#         new_query = new_query[:-1] + "." if query_words[-1][-1] in ".?!" else new_query + "."

#     return new_query.capitalize()


# def UniversalTranslator(Text):
#     """Translate recognized text into English."""
#     return mt.translate(Text, "en", "auto").capitalize()


# # ── Core STT function ─────────────────────────────────────────────────────────
# def SpeechRecognition():
#     """
#     Captures audio from the microphone and returns the recognized + formatted text.

#     Latency improvements over Selenium/browser version:
#       - No browser launch overhead (~10-15s eliminated)
#       - Microphone kept warm — no per-call device open/close
#       - Ambient noise calibration done once at startup, not per call
#       - Direct Google Speech API call — no HTML/JS round-trip
#     Expected latency: ~1-3s (vs original ~34s)
#     """
#     with _microphone as source:
#         SetAssistantStatus("Listening...")
#         try:
#             # timeout      : how long to wait for speech to START (seconds)
#             # phrase_time_limit : max length of a single utterance (seconds)
#             audio = recognizer.listen(source, timeout=2, phrase_time_limit=20)
#         except sr.WaitTimeoutError:
#             return ""   # No speech detected — caller should loop

#     try:
#         SetAssistantStatus("Recognizing...")
#         # recognize_google uses the same Google Speech backend as the browser Web Speech API
#         # The `language` param accepts the same locale strings e.g. "en-US", "hi-IN"
#         Text = recognizer.recognize_google(audio, language=InputLanguage)

#         if not Text:
#             return ""

#         if "en" in InputLanguage.lower():
#             return QueryModifier(Text)
#         else:
#             SetAssistantStatus("Translating...")
#             return QueryModifier(UniversalTranslator(Text))

#     except sr.UnknownValueError:
#         # Audio captured but Google couldn't interpret it
#         return ""
#     except sr.RequestError as e:
#         print(f"[STT] Google Speech API error: {e}")
#         SetAssistantStatus("Speech API Error")
#         return ""


# # ── Entrypoint ────────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     print("[STT] Ready. Speak now...")
#     while True:
#         Text = SpeechRecognition()
#         if Text:
#             print(Text)



import speech_recognition as sr
import mtranslate as mt
import os
import time
from dotenv import dotenv_values

# ── Load env variables ────────────────────────────────────────────────────────
env_vars = dotenv_values(".env")
InputLanguage = (env_vars.get("InputLanguage") or "en-US").strip()

# ── Path setup ────────────────────────────────────────────────────────────────
current_dir = os.getcwd()
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
os.makedirs(TempDirPath, exist_ok=True)

STATUS_FILE = os.path.join(TempDirPath, "Status.data")

def SetAssistantStatus(Status: str):
    """Write assistant status to a file for the frontend to read."""
    try:
        with open(STATUS_FILE, "w", encoding="utf-8") as file:
            file.write(Status)
    except Exception:
        # If frontend file path isn't available for some reason, don't crash STT.
        pass


def QueryModifier(Query: str) -> str:
    """Ensure proper punctuation and formatting on the recognized query."""
    new_query = (Query or "").lower().strip()
    if not new_query:
        return ""

    question_words = [
        "how", "what", "who", "where", "why", "which", "whose", "whom",
        "can you", "what's", "where's", "how's", "do you", "if"
    ]

    is_question = any(qw in new_query for qw in question_words)

    last_char = new_query[-1]
    if is_question:
        if last_char not in ".?!":
            new_query += "?"
        else:
            new_query = new_query[:-1] + "?"
    else:
        if last_char not in ".?!":
            new_query += "."
        else:
            new_query = new_query[:-1] + "."

    return new_query.capitalize()


def UniversalTranslator(Text: str) -> str:
    """Translate recognized text into English."""
    if not Text:
        return ""
    return mt.translate(Text, "en", "auto").capitalize()


# ── Recognizer (INIT ONCE) ────────────────────────────────────────────────────
recognizer = sr.Recognizer()

# These help reduce false triggers and missed speech
recognizer.pause_threshold = 0.7           # silence before phrase ends
recognizer.non_speaking_duration = 0.35    # amount of silence stored around phrase
recognizer.phrase_threshold = 0.25         # minimum "speechy" audio to count as a phrase

# Start with dynamic threshold to calibrate, then freeze (important fix)
recognizer.dynamic_energy_threshold = True

# ── Microphone (OPEN ONCE + CALIBRATE ONCE) ──────────────────────────────────
_microphone = sr.Microphone()

print("[STT] Calibrating microphone for ambient noise...")
with _microphone as source:
    # You can raise duration to 1.5–2.0 if your room noise fluctuates
    recognizer.adjust_for_ambient_noise(source, duration=1.0)

# Freeze threshold to prevent it drifting too low and causing false triggers
recognizer.dynamic_energy_threshold = False

# Add a margin so random noise doesn't trigger "speech started"
ENERGY_MARGIN = 200
recognizer.energy_threshold = float(recognizer.energy_threshold) + ENERGY_MARGIN

print(f"[STT] Microphone ready. language={InputLanguage} energy_threshold={recognizer.energy_threshold:.0f}")

# ── Helper to estimate audio duration (used to ignore noise blips) ────────────
def _audio_duration_seconds(audio: sr.AudioData) -> float:
    try:
        # frame_data length = sample_rate * sample_width * seconds
        return len(audio.frame_data) / (audio.sample_rate * audio.sample_width)
    except Exception:
        return 0.0


# ── Core STT function ─────────────────────────────────────────────────────────
def SpeechRecognition() -> str:
    """
    Captures audio from the microphone and returns the recognized + formatted text.

    Fixes included:
      - Prevent false "Recognizing..." when user didn't speak (noise blips)
      - Freeze energy threshold after calibration to avoid drift
      - Reject very short audio captures before calling Google
      - Reset status back to Listening on non-results/errors
    """
    # 1) LISTEN
    with _microphone as source:
        SetAssistantStatus("Listening...")
        try:
            # timeout: seconds to wait for speech to START
            # phrase_time_limit: max duration of an utterance
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            # No speech started within timeout; keep listening in caller loop
            SetAssistantStatus("Listening...")
            return ""

    # 2) FILTER OUT NOISE BLIPS (CRITICAL FIX)
    dur = _audio_duration_seconds(audio)
    # If you still see false triggers, raise this to 0.5
    MIN_UTTERANCE_SEC = 0.35
    if dur < MIN_UTTERANCE_SEC:
        SetAssistantStatus("Listening...")
        return ""

    # 3) RECOGNIZE
    try:
        SetAssistantStatus("Recognizing...")
        text = recognizer.recognize_google(audio, language=InputLanguage)

        if not text or not text.strip():
            SetAssistantStatus("Listening...")
            return ""

        # 4) TRANSLATE IF NEEDED + FORMAT
        if "en" in InputLanguage.lower():
            return QueryModifier(text)
        else:
            SetAssistantStatus("Translating...")
            translated = UniversalTranslator(text)
            SetAssistantStatus("Listening...")
            return QueryModifier(translated)

    except sr.UnknownValueError:
        # Google couldn't understand (often silence/noise)
        SetAssistantStatus("Listening...")
        return ""
    except sr.RequestError as e:
        # Network/API failure
        print(f"[STT] Google Speech API error: {e}")
        SetAssistantStatus("Speech API Error")
        # short cooldown so you don't spam requests if network is down
        time.sleep(0.3)
        SetAssistantStatus("Listening...")
        return ""
    except Exception as e:
        print(f"[STT] Unexpected error: {e}")
        SetAssistantStatus("Listening...")
        return ""


# ── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("[STT] Ready. Speak now...")
    while True:
        out = SpeechRecognition()
        if out:
            print(out)
