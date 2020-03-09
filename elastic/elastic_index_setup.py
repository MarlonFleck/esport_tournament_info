"""
HELPER SCRIPT

This script initializes puts six test data sets to the elasticsearch database (two with same ID, so five data sets will
be in the database if it was empty before)
"""

from elastic import elastic_server
import json

file_name = [
    r'C:\Users\Marlon\Documents\projects\data_record\python\messages\message1.json',
    r'C:\Users\Marlon\Documents\projects\data_record\python\messages\message2.json',
    r'C:\Users\Marlon\Documents\projects\data_record\python\messages\message3.json',
    r'C:\Users\Marlon\Documents\projects\data_record\python\messages\message4.json',
    r'C:\Users\Marlon\Documents\projects\data_record\python\messages\message5.json',
    r'C:\Users\Marlon\Documents\projects\data_record\python\messages\message6.json']

for this_file_name in file_name:
    with open(this_file_name) as this_json_file:
        this_data = json.load(this_json_file)

    elastic_server.post_json(this_data)

