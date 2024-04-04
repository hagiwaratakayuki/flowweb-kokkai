
from utillib import hash
import numpy as np
from typing import TypedDict


class SentimentData(TypedDict):
    position: list
    direction: list


class NodeData(TypedDict):
    vector: list
    sentiment: SentimentData


def get_ymd(ymd_list: list[str]):
    ['-'.join(ymd_list[:i]) for i in range(1, 4)]


def get_hash(vector: np.ndarray):
    return hash.encode(vector[0], vector[1])
