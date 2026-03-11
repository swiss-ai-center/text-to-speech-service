from common_code.config import get_settings
from common_code.logger.logger import get_logger, Logger
from common_code.service.models import Service
from common_code.service.enums import ServiceStatus
from common_code.common.enums import FieldDescriptionType, ExecutionUnitTagName, ExecutionUnitTagAcronym
from common_code.common.models import FieldDescription, ExecutionUnitTag
from common_code.tasks.models import TaskData
# Imports required by the service's model
import tts_calls
from pydub import AudioSegment
from io import BytesIO
import json
from mutagen import File as MutagenFile

api_description = """
Queries an online API based on Edge-TTS and returns an audio file based on user-submitted text.
The entry must be a JSON file containing the following fields:
- input: the text to be converted to speech
- (optional) voice: [Open AI voice names](https://tts.travisvn.com/). Default voice is in french
- (optional) speed: playback speed (0.25 to 4.0). Default speed is 1.0
"""
api_summary = """Queries an online API based on Edge-TTS and returns an audio file based on user-submitted text.
"""
api_title = "Text to Speech API."
version = "0.0.1"

settings = get_settings()


def detect_audio_format(data: bytes) -> str:
    temp = BytesIO(data)
    audio = MutagenFile(temp)
    if audio is None:
        raise ValueError("Unsupported audio format")
    return audio.mime[0].split("/")[-1]  # returns 'mp3', 'wav', etc.


class MyService(Service):
    """
    Text-to-speech application
    """

    # Any additional fields must be excluded for Pydantic to work
    _model: object
    _logger: Logger

    def __init__(self):
        super().__init__(
            name="Text To Speech",
            slug="text-to-speech",
            url=settings.service_url,
            summary=api_summary,
            description=api_description,
            status=ServiceStatus.AVAILABLE,
            data_in_fields=[
                FieldDescription(
                    name="parameters",
                    type=[
                        FieldDescriptionType.APPLICATION_JSON
                    ],
                ),
            ],
            data_out_fields=[
                FieldDescription(
                    name="result", type=[FieldDescriptionType.AUDIO_MP3]
                ),
            ],
            tags=[
                ExecutionUnitTag(
                    name=ExecutionUnitTagName.NATURAL_LANGUAGE_PROCESSING,
                    acronym=ExecutionUnitTagAcronym.NATURAL_LANGUAGE_PROCESSING,
                ),
            ],
            has_ai=True,
            docs_url="https://docs.swiss-ai-center.ch/reference/services/text-to-speech/",
        )
        self._logger = get_logger(settings)

    def process(self, data):
        # NOTE that the data is a dictionary with the keys being the field names set in the data_in_fields
        # The objects in the data variable are always bytes. It is necessary to convert them to the desired type

        parameters = json.loads(data['parameters'].data)
        audio_raw_mp3 = tts_calls.tts(parameters)

        # NOTE that the result must be a dictionary with the keys being the field names set in the data_out_fields
        audio = AudioSegment.from_file(BytesIO(audio_raw_mp3), format=detect_audio_format(audio_raw_mp3))

        return {
            "result": TaskData(data=audio.export(format='mp3').read(), type=FieldDescriptionType.AUDIO_MP3)
        }

