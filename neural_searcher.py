from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchAny, Range
from sentence_transformers import SentenceTransformer

class NeuralSearcher:

    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        self.qdrant_client = QdrantClient(host='localhost', port=6333)

    def search(
            self,
            text: str,
            filter_set: [],
            order_set: [],
            limit: int = 5,
            ):
        vector = self.model.encode(text).tolist()

        results = self.qdrant_client.search(
                    collection_name=self.collection_name,
                    query_vector=vector,
                    query_filter=self._filters(filter_set),
                    limit=limit
                    )

        return self._process_results(results, order_set)

    def _filters(self, filter_set): 
        [price_lower, price_upper, min_score, country] = filter_set
        must_cons = []
        must_cons.append(
                FieldCondition(
                    key="price",
                    range=Range(
                        gt=None,
                        gte=price_lower,
                        lt=None,
                        lte=price_upper
                        )
                    )
                )

        if min_score != None:
            must_cons.append(
                    FieldCondition(
                        key="points",
                        range=Range(
                            gt=None,
                            gte=min_score,
                            lt=None,
                            lte=None
                            )
                        )
                    )

        if country != None:
            split_c = country.split(" ")
            if len(split_c) == 1:
                must_cons.append(
                        FieldCondition(
                            key="country",
                            match=MatchValue(value=split_c[0])
                            )
                        )
            else:
                must_cons.append(
                        FieldCondition(
                            key="country",
                            match=MatchAny(any=split_c)
                            )
                        )

        return Filter(must=must_cons)

    def _process_results(self, results, order_set):
        [order_on, order_by] = order_set
        payloads = [hit.payload for hit in results]
        reverse = True
        if order_by == 'asc':
            reverse = False

        if order_on != None:
            payloads = sorted(payloads, key=lambda k: k[order_on], reverse=reverse)
        elif order_by == 'asc':
            payloads = payloads[::-1]

        return payloads


