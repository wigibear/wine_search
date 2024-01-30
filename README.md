# Introduction and motivation
This repo is meant to demonstrate how vector search could be used to find wines with a given description and fitting within desired parameters, and is based on [this](https://huggingface.co/datasets/GroNLP/ik-nlp-22_winemag/tree/main) dataset. In theory as all of these scripts were executed on my machine it isn't strictly necessary to do the wine list updates via rabbitmq and celery, however in practice this might not necessarily be the case, and serves as a proof of concept.

# Startup instructions for necessary docker containers
In order to have the wine search work we need to have one docker container running the qdrant database which is initiated as follows:
```
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
```
And another to run in the background to receive updates via rabbitmq and celery:
```
docker run -d -p 5673:5672 rabbitmq
```

# Initial housekeeping
First things first, we need to make sure we have the requirements installed, so in the environment of your choice (if using):
```
python3 -m pip install -r requirements
```

# Celery worker
In addition to the docker containers we also need to have the celery worker running which can be triggered using the following:
```
celery -A data_updator worker --loglevel-INFO
```

# Qdrant client setup and upload
These scripts are necessary to create the client, associated with the docker container, create our vectors, and upload them to the client.
```
python3 vector_generation.py
python3 upload_data.py
```

# Using the search client
Now that the database has been created we can interact with it by firing up our endpoint:
```python3 sommelier.py```
This can be accessed at `http://0.0.0.0:8000/docs`

# Adding a new wine to the database
Last but not least, should you wish to add a new wine to the database, for example the wine stored at `qdrant_storage/new_wine.json` then you can use the following script to initiate an update via celery:
```
python3 add_wine.py
```
