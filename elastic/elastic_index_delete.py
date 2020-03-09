"""
HELPER SCRIPT

Script that will delete the elasticsearch index.
"""

from elasticsearch import Elasticsearch
from settings import es_index

# Delete the index.
es = Elasticsearch()
es.indices.delete(index=es_index, ignore=[400, 404])
print('The index "{}" has been deleted.'.format(es_index))
