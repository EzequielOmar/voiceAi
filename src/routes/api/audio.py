from . import api_blueprint
from flask import request, send_file
from src.services import vosk_service
from src.services import audio_service
from src.errors.errors import (
    AudioValidationError,
)
from src.services.tts_service import synthesize_text


@api_blueprint.route("/audio", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        raise AudioValidationError("Missing 'audio' file in request.")
    audio_file = request.files["audio"]
    audio_wav = audio_service.convert_audio_to_wav(audio_file)
    transcription = vosk_service.transcribe_audio(audio_wav)
    if transcription == "":
        raise AudioValidationError("The audio is empty.")
    audio_io = synthesize_text(transcription)
    return send_file(audio_io, mimetype="audio/wav")
