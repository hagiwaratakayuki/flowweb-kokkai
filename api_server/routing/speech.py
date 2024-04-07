from fastapi import APIRouter, status

from .query.speech import get_by_discussion_async, get_speech, get_speech_multi

from .return_models.types.speech

router = APIRouter()


@router.get('/all_summary')
def all_as_vertex() -> list[NodeOverview]:
