from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import numpy as np
import pandas as pd
import json

qdr_client = QdrantClient(host='localhost', port=6333)

qdr_client.recreate_collection(
        collection_name='wine list',
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

df = pd.read_csv('qdrant_storage/wine_data.csv')
df.to_json('qdrant_storage/wine_data.json', orient='records', lines=True)

fd = open('qdrant_storage/wine_data.json')

payload = map(json.loads, fd)
vectors = np.load('qdrant_storage/wine_vectors.npy')


qdr_client.upload_collection(
        collection_name='wine list',
        vectors=vectors,
        payload=payload,
        ids=None,
        batch_size=256
        )

