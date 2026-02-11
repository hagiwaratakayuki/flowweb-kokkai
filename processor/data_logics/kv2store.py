from collections import deque
from collections.abc import Iterable
import time
import math
from doc2vec.vectaizer.gensim import loadWord2VecFormat, MODEL_PATH
from db.word_to_vec import WordToVec
from db.model import put_multi
from multiprocessing import Pool
import multiprocessing as multi


def chunker(itr: Iterable, chunk_size: int = 50, bulk_size=400):
    index = 0
    bulk_count = 0
    bulk = deque()
    chunk = deque()
    for row in itr:
        index += 1
        chunk.append(row)
        if index >= chunk_size:
            index = 0
            bulk_count += 1
            bulk.append(chunk)
            chunk = deque()
            if bulk_count >= bulk_size:
                yield bulk
                bulk = deque()
                bulk_count = 0
    if index > 0:
        bulk.append(chunk)
        bulk_count += 1

    if bulk_count > 0:
        yield bulk


def slot(bulk_itr: Iterable, time_range: float = 1):
    for bulk in bulk_itr:
        start = time.time()
        for content in bulk:
            yield content
        diff = time.time() - start
        if diff < time_range:
            time.sleep(time_range)


def kv2itr(model_path=MODEL_PATH, ):
    kv = loadWord2VecFormat(model_path)
    for key in kv.key_to_index.keys():
        vector = kv.get_vector(key)
        if isinstance(key, str) == False:
            continue
        yield WordToVec(word=key, vector=vector)  # type: ignore


def kv2store(chunk_size: int = 50, bulk_size=400, time_range: float = 1, model_path=MODEL_PATH, workers=multi.cpu_count()):
    itr = kv2itr(model_path=model_path)
    chunked_itr = chunker(itr=itr, chunk_size=chunk_size, bulk_size=bulk_size)
    sloted_itr = slot(chunked_itr, time_range=time_range)
    process_chunk_size = math.floor(
        float(bulk_size) / float(multi.cpu_count())) or 1
    with Pool(processes=workers) as p:
        process_itr = p.imap_unordered(
            _put_multi, iterable=sloted_itr, chunksize=process_chunk_size)

        for void in process_itr:
            a = 1


def _put_multi(models):
    put_multi(models=models)
