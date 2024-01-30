from fastapi import FastAPI
from neural_searcher import NeuralSearcher

app = FastAPI()
ns = NeuralSearcher(collection_name='wine list')

@app.get("/api/search")
def search_wine_list(
        q: str,
        limit: int = 5,
        p_from: int = None,
        p_to: int = None,
        min_score: int = None,
        country: str = None,
        order_on: str = None,
        order_by: str = 'desc'
        ):
    
    filter_set = [p_from, p_to, min_score, country]
    order_set = [order_on, order_by]
    results = ns.search(
            text=q,
            filter_set=filter_set,
            order_set=order_set,
            limit=limit
            )

    return {"result": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

