
from ..cluster.overviews import ClusterOverviews
from .single import SpeechSingle
from pydantic import BaseModel


class SpeechData(BaseModel):
    speech: SpeechSingle
    clusters: ClusterOverviews
