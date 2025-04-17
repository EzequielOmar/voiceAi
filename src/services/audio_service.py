import io
from werkzeug.datastructures import FileStorage
from pydub import AudioSegment
from typing import IO
from src.errors.errors import AudioDecodeError, AudioConversionError


def convert_audio_to_wav(file_storage: FileStorage) -> IO[bytes]:
    """
    Convert any uploaded audio file (FileStorage) to 16kHz mono 16-bit PCM WAV.

    :param file_storage: Flask/Werkzeug FileStorage from request.files
    :return: BytesIO containing the WAV audio
    :raises AudioDecodeError: If pydub cannot read the input format
    :raises AudioConversionError: If export to WAV fails
    """
    # Read all incoming bytes
    try:
        raw_bytes = file_storage.read()
    except Exception as e:
        raise AudioDecodeError(f"Unable to read uploaded file: {e}")

    audio_stream = io.BytesIO(raw_bytes)

    # Decode using pydub without explicit format (let ffmpeg detect)
    try:
        audio = AudioSegment.from_file(audio_stream)
    except Exception as e:
        raise AudioDecodeError(f"Decoding failed: {e}")

    # Convert audio properties for Vosk compatibility
    try:
        converted = audio.set_frame_rate(16000)
        converted = converted.set_channels(1)
        converted = converted.set_sample_width(2)
    except Exception as e:
        raise AudioConversionError(f"Format conversion failed: {e}")

    # Export to WAV in-memory
    wav_io = io.BytesIO()
    try:
        converted.export(wav_io, format="wav")
    except Exception as e:
        raise AudioConversionError(f"Export to WAV failed: {e}")

    # Rewind for downstream processing
    wav_io.seek(0)
    return wav_io
