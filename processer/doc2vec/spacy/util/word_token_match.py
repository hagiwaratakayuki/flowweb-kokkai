from re import A
import re
from typing import Iterable, List, Literal
from spacy.tokens import Token

type FaceType = Literal["norm_", "lemma_", "orth_"]
type TargetFaces = List[FaceType]
DEFAULT_TARGET_FACES: TargetFaces = ["norm_"]

type PermissionLevel = Literal[0, 1, 2, 3]
STRICT: PermissionLevel = 0
ALLOW_LEFTHAND: PermissionLevel = 1
ALLOW_RIGHTHAND: PermissionLevel = 2
ALLOW_BOTH: PermissionLevel = 3


def check(token: Token, word: str, target_faces: TargetFaces = DEFAULT_TARGET_FACES):
    res = check_with_slidecount(
        token=token, word=word, target_faces=target_faces)
    return res[0]


def check_with_slidecount(token: Token, word: str, target_faces: TargetFaces = DEFAULT_TARGET_FACES, permission_level: PermissionLevel = STRICT):

    doc = token.doc
    cursor_limit = len(doc)
    for target_face in target_faces:
        token_target_face: str = getattr(token, target_face)
        if token_target_face == word:
            return True, 0
        if word in token_target_face:

            if permission_level == ALLOW_BOTH or (permission_level == ALLOW_LEFTHAND and len(word) + token_target_face.index(word) == len(token_target_face)):
                return True, 0
            if permission_level == ALLOW_RIGHTHAND and token_target_face.startswith(word):
                return True, 0
            continue

        if (permission_level == ALLOW_RIGHTHAND or permission_level == STRICT):
            if word.startswith(token_target_face) == False:
                continue
        else:
            head_word = word[0]
            lefthand_index = token_target_face.find(head_word)
            if lefthand_index == -1:
                continue

            lefthand_token_face = token_target_face[lefthand_index:]
            if lefthand_token_face not in word:
                continue

        count_ = 1
        cursor = token.i + count_
        while cursor < cursor_limit:
            tok = doc[cursor]
            token_target_face += getattr(tok, target_face)
            if token_target_face == word:
                return True, count_
            if token_target_face in word:

                count_ += 1
                cursor = token.i + count_
                continue

            if word in token_target_face:
                if permission_level == ALLOW_BOTH:
                    return True, count_
                if permission_level == ALLOW_LEFTHAND:
                    if not token_target_face.split(word)[-1]:
                        return True, count_
                break

            if permission_level == ALLOW_LEFTHAND or permission_level == ALLOW_BOTH:

                lefthand_token_face += getattr(tok, target_face)
                if lefthand_token_face == word:
                    return True, count_
                if lefthand_token_face in word:
                    count_ += 1
                    continue

            break

    return False, 0
