class APIError(Exception):
    """Base for all application errors."""

    status_code: int = 500
    message: str = "Internal Server Error"

    def __init__(self, detail: str = None):
        if detail:
            self.message = detail
        super().__init__(self.message)

    def to_dict(self):
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "code": self.status_code,
        }


class FileNotFoundError(APIError):
    status_code = 500
    message = "File not found"


# === Custom Exceptions for Audio Service ===
class AudioDecodeError(APIError):
    status_code = 400
    message = "Failed to decode uploaded audio file"


class AudioConversionError(APIError):
    status_code = 500
    message = "Error converting audio to WAV format"


# === Custom Exceptions for Vosk Service ===
class ModelNotInitializedError(APIError):
    status_code = 500
    message = "Vosk model not initialized. Call init_model() first."


class AudioValidationError(APIError):
    status_code = 400
    message = "Audio file did not pass validation."


class TranscriptionError(APIError):
    status_code = 502
    message = "Failed to transcribe audio."


# === Custom Exceptions for TTS Service ===
class TTSServiceError(APIError):
    status_code = 502
    message = "TTS service returned an error"


class TTSServiceUnavailableError(TTSServiceError):
    status_code = 503
    message = "TTS service is unavailable"
