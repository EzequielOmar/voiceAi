import os
import io
import requests
from typing import IO
from src.errors.errors import TTSServiceError, TTSServiceUnavailableError


import pprint


def synthesize_text(text: str) -> IO[bytes]:
    """
    Send text to an external TTS service and return the synthesized audio as a BytesIO object.

    :param text: The text to synthesize into speech.
    :return: BytesIO containing the raw audio (e.g., WAV or MP3) returned by the TTS service.
    :raises TTSServiceUnavailableError: If the service cannot be reached.
    :raises TTSServiceError: If the service returns a non-200 status or empty payload.
    """
    # Configure endpoint via environment or default to localhost
    tts_url = os.getenv("TTS_URL", "http://tts:5002/api/tts")

    try:
        response = requests.post(
            tts_url,
            data={
                "text": text,
                # "speaker_id": "",
                # "style_wav": "",
                # "language_id": "",
            },
            timeout=10,
        )
    except requests.RequestException as e:
        raise TTSServiceUnavailableError(f"Failed to connect to TTS service: {e}")

    if response.status_code != 200:
        raise TTSServiceError(
            f"TTS service responded with status {response.status_code}: {response.text}"
        )

    audio_data = response.content
    if not audio_data:
        raise TTSServiceError("TTS service returned empty audio payload")

    # Wrap raw bytes in a BytesIO for downstream processing
    audio_io = io.BytesIO(audio_data)
    audio_io.seek(0)
    return audio_io
