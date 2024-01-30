from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
import json
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from celery import Celery
 
qdr_client = QdrantClient(host='localhost', port=6333)

qdr_client.recreate_collection(
        collection_name='wine list',
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

app = Celery('data_updator', broker='pyamqp://guest@localhost//')

model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')

@app.task
def add(wine):
    #vector updates
    cur_vecs = np.load('qdrant_storage/wine_vectors.npy', allow_pickle=False)
    new_vec = model.encode(wine['province'] + " || " + wine['variety'] + " || " + wine['description'])
    new_vec = np.reshape(new_vec, (1,384))
    vecs = np.concatenate((cur_vecs, new_vec), axis=0)
    np.save('qdrant_storage/wine_vectors.npy', vecs, allow_pickle=False)

    # payload updates
    cur_pay = pd.read_json('qdrant_storage/wine_data.json', lines=True)
    new_wine = pd.DataFrame.from_dict(wine, orient='index').transpose()
    new_pay = pd.concat([cur_pay, new_wine])
    new_pay.to_json('qdrant_storage/wine_data.json', orient='records', lines=True)
    fd = open('qdrant_storage/wine_data.json')
    payload = map(json.loads, fd)

    # client updates
    qdr_client.upload_collection(
            collection_name='wine list',
            vectors=vecs,
            payload=payload,
            ids=None,
            batch_size=256
            )

