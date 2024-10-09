

from typing import Optional, List
from .overview import SpeechOverview
from ..cluster.overviews import ClusterOverviews
from .single import SpeechSingle
from pydantic import BaseModel


class SpeechData(BaseModel):
    speech: SpeechSingle
    clusters: ClusterOverviews
    discussion: Optional[List[SpeechOverview]] = None
