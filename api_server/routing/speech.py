from fastapi import APIRouter, status

from .query.speech import get_by_discussion_async, get_speech, get_speech_multi

from .return_models.types.speech.single import SpeechS

router = APIRouter()


@router.get('/data')
def all(id: int) -> :
