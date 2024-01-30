from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from tqdm.notebook import tqdm

model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')

df = pd.read_csv('qdrant_storage/wine_data.csv')

vecs = model.encode(
        [r.province + " || " + r.variety + " || " + r.description for r in df.itertuples()],
        batch_size=256,
        show_progress_bar=True
        )

np.save('qdrant_storage/wine_vectors.npy', vecs, allow_pickle=False)
