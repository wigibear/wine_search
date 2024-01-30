# Startup instructions for qdrant docker image
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant

# Startup instructions for rabbitmq docker image
docker run -d -p 5673:5672 rabbitmq

# Startup for celery worker
celery -A data_updator worker --loglevel-INFO

# Initial setup
python3 -m pip install -r requirements
python3 vector_generation.py
python3 upload_data.py

# Using the search client
python3 sommelier.py
`Then you can interact with the API at http://0.0.0.0:8000/docs`

# Adding a new wine to the database
python3 add_wine.py
