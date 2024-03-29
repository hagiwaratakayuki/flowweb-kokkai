
from typing import TypedDict
from typing import List as typing_List  


class Meeting(TypedDict):
    session: int
    issue: int
    name: str
    start: str
    end: str
    response_from: str
    url: str
    pdf: str
    header_text: str
    moderators: typing_List[str]
    moderator_ids: typing_List[str]


