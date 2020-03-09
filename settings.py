"""
ELASTICSEARCH
"""
es_index = 'gamerecords'
es_host_add = 'localhost'
es_port = 9200

"""
RABBITCONNECT
"""
rc_host_add = 'localhost'
rc_port = 5672

"""
API FILTER
"""
# Define filter keywords that a query has to match (if defined)
filter_keywords_must = ['title', 'state']

"""
LOGGER
"""
logger_name = 'game_record'
log_file_name = 'logfile.log'
