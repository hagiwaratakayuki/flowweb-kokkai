

from typing import Literal, Optional, List, Union

from ..node.overview import NodeOverview

from ..node.overviews import NodeOverviews


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
    link_from: NodeOverviews
    link_to: List[NodeOverview]
