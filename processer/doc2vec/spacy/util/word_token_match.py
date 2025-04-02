from re import A
import re
from typing import Iterable, List, Literal
from spacy.tokens import Token

type FaceType = Literal["norm_", "lemma_", "orth_"]
type FaceTypes = List[FaceType]
DEFAULT_FACETYPES: FaceTypes = ["norm_"]

type PEEMISSION_LEVEL = Literal[0, 1, 2, 3]
STRICT: PEEMISSION_LEVEL = 0
ALLOW_LEFTHAND: PEEMISSION_LEVEL = 1
ALLOW_RIGHTHAND: PEEMISSION_LEVEL = 2
ALLOW_BOTH: PEEMISSION_LEVEL = 3


def check(token: Token, word: str, target_faces: FaceTypes = DEFAULT_FACETYPES):
    res = check_with_slidecount(
        token=token, word=word, target_faces=target_faces)
    return res[0]


def check_with_slidecount(token: Token, word: str, target_faces: FaceTypes = DEFAULT_FACETYPES, permission_level=0):

    doc = token.doc
    index_limit = len(doc)
    for target_face in target_faces:
        token_target_face: str = getattr(token, target_face)
        if word in token_target_face:

            if token_target_face == word:
                return True, 0
            if permission_level == ALLOW_BOTH or permission_level == ALLOW_LEFTHAND:
                return True, 0
            if permission_level == ALLOW_RIGHTHAND and token_target_face.startswith(word):
                return True, 0
            continue
        if word.startswith(token_target_face) == False:
            continue
        else:
            if permission_level == ALLOW_RIGHTHAND or permission_level == ALLOW_BOTH:
                return True, 0
        count_ = 1
        cursor = token.i + count_
        while cursor < index_limit:
            tok = doc[cursor]
            token_target_face += getattr(tok, target_face)
            if token_target_face in word:
                if token_target_face == word:
                    return True, count_
                count_ += 1
                cursor = token.i + count_
                continue
            if word in token_target_face:
                return permission_level == ALLOW_RIGHTHAND or permission_level == ALLOW_BOTH, count_
            break

    return False, 0
