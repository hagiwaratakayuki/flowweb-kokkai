

from typing import Optional, List


from .overview import SpeechOverview

from .single import SpeechSingle
from ..cluster.overviews import ClusterOverviews
from ..speaker.single import SpeakerSingle
from pydantic import BaseModel


class SpeechData(BaseModel):
    speech: SpeechSingle
    clusters: ClusterOverviews
    discussion: Optional[List[SpeechOverview]] = None
    keywords: Optional[List[str]]
    speaker: SpeakerSingle
