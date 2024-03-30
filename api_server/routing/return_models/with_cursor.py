from typing import Literal, Union


class WithCursor:
    cursor: Union[str, Literal[False]]
