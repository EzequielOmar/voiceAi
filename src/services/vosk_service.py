import wave
import json
from typing import BinaryIO, Optional
from vosk import Model, KaldiRecognizer
from src.errors.errors import (
    FileNotFoundError,
    ModelNotInitializedError,
    AudioValidationError,
    TranscriptionError,
)

# === Global Model Holder ===
model: Optional[Model] = None


def init_model(model_path: str = "/app/models/spanish") -> Model:
    """
    Load the Vosk model once at application startup.

    :param model_path: Filesystem path to the Vosk model directory.
    :return: Initialized Vosk Model instance.
    :raises FileNotFoundError: If the model directory is not found.
    """
    global model
    if model is None:
        try:
            model = Model(model_path)
        except Exception as e:
            raise FileNotFoundError(f"Could not load Vosk model from {model_path}: {e}")
    return model


def validate_format(wav_file: wave.Wave_read) -> None:
    """
    Ensure the WAV file meets Vosk requirements.

    :param wav_file: Open wave.Wave_read instance.
    :raises AudioValidationError: If any format requirement is not met.
    """
    if wav_file.getnchannels() != 1:
        raise AudioValidationError("Audio file must be mono (1 channel)")
    if wav_file.getsampwidth() != 2:
        raise AudioValidationError("Audio file must be 16-bit PCM (sample width=2)")
    if wav_file.getframerate() not in (8000, 16000, 44100):
        raise AudioValidationError(
            f"Unsupported sample rate: {wav_file.getframerate()}. "
            "Expected one of: 8000, 16000, 44100 Hz"
        )


def perform_transcription(wav_file: wave.Wave_read) -> str:
    """
    Run the Vosk recognizer on the validated WAV file.

    :param wav_file: wave.Wave_read instance at position=0.
    :return: Transcribed text.
    :raises TranscriptionError: On recognition failures.
    """
    rec = KaldiRecognizer(model, wav_file.getframerate())
    rec.SetWords(True)

    chunks = []
    try:
        while True:
            data = wav_file.readframes(4000)
            if not data:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                chunks.append(res.get("text", ""))
        final = json.loads(rec.FinalResult())
        chunks.append(final.get("text", ""))
    except Exception as e:
        raise TranscriptionError(f"Error during transcription: {e}")

    return " ".join(filter(None, chunks)).strip()


def transcribe_audio(file_obj: BinaryIO) -> str:
    """
    High-level function to validate and transcribe an audio stream.

    :param file_obj: File-like object (e.g., BytesIO or open file) containing WAV data.
    :return: Transcribed text.
    :raises ModelNotInitializedError: If init_model() was not called.
    :raises AudioValidationError: If the audio fails format checks.
    :raises TranscriptionError: On transcription or I/O errors.
    """
    # Ensure model loaded
    if model is None:
        raise ModelNotInitializedError()

    # Reset stream pointer
    try:
        file_obj.seek(0)
    except Exception:
        pass

    # Open as WAV
    with wave.open(file_obj, "rb") as wf:
        validate_format(wf)
        return perform_transcription(wf)
