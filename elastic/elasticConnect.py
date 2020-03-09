"""
CLASS THAT CONNECTS TO THE ELASTICSEARCH DATABASE AND HANDLES ALL GET AND PUT REQUESTS TO IT
"""
from settings import es_host_add, es_port, es_index, filter_keywords_must, logger_name
from .gamerecordDocument import Gamerecord
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Q
from datetime import datetime
import logging


def parse_time(time_str):
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')


def datetime_to_str(time_datetime):
    return time_datetime.strftime('%Y-%m-%d %H:%M:%S')


class ElasticConnect:

    def __init__(self):
        # Setup the logger.
        logger_name_elastic = logger_name + '.elastic'
        self.elastic_logger = logging.getLogger(logger_name_elastic)
        connections.create_connection(hosts=es_host_add, port=es_port)
        # Setup the index for the game records.
        Gamerecord.init()
        self.Gamerecord = Gamerecord

    def get_by_id(self, document_id):
        # Get a document by a specific ID.
        document = self.Gamerecord.get(id=str(document_id))
        return document

    def get_filtered(self, filters: dict):
        # Query the elasticsearch database. This will return all saved documents. If filters are set, those will be
        # applied to the query.
        self.elastic_logger.info('Received request with filters: {}'.format(filters))
        # Create a search object.
        s = self.Gamerecord.search(index=es_index)
        # Create query filter.
        must_queries = []
        for this_filter_keyword in filter_keywords_must:
            if filters[this_filter_keyword]:
                this_filter = {this_filter_keyword: filters[this_filter_keyword]}
                this_query = Q('match', **this_filter)
                must_queries.append(this_query)

        # If a filter value for tournament is given, this will filter the tournament name.
        if filters['tournament']:
            must_queries.append(
                Q("nested", path="tournament", query=Q("match", tournament__name=filters['tournament'])))

        s.query = Q('bool', must=must_queries)

        # Filter by time range.
        if filters['date_start_gte']:
            filters['date_start_gte'] = parse_time(filters['date_start_gte'])
        if filters['date_start_lte']:
            filters['date_start_lte'] = parse_time(filters['date_start_lte'])

        s = s.filter('range', date_start_text={'gte': filters['date_start_gte'], 'lte': filters['date_start_lte']})
        # Execute the search
        res = s.execute()

        if len(res.hits) == 0:
            self.elastic_logger.info("No data found for this query")
            return "No data found for this query"

        # Initiate the result dict that will be given as an API response (as a JSON)
        res_dict = dict()
        res_counter = 0
        for this_res in res.hits:
            res_counter += 1
            this_res_dict = dict()
            this_res_dict['id'] = this_res['id']
            this_res_dict['title'] = this_res['title']
            this_res_dict['tournament'] = this_res['tournament']['name']
            this_res_dict['date_start_gte'] = datetime_to_str(this_res['date_start_text'])
            # Convert team information into dict (to transform into JSON later).
            teams = list()
            for this_team in this_res['teams']:
                team_dict = dict()
                team_dict['name'] = this_team['name']
                team_dict['id'] = this_team['id']

                teams.append(team_dict)

            this_res_dict['teams'] = teams
            # Convert score information into dict (to transform into JSON later).
            scores = list()
            for this_score in this_res['scores']:
                score_dict = dict()
                score_dict['team'] = this_score['team']
                score_dict['score'] = this_score['score']
                score_dict['winner'] = this_score['winner']

                scores.append(score_dict)

            this_res_dict['scores'] = scores

            res_dict['result_{}'.format(res_counter)] = this_res_dict

        self.elastic_logger.info("{} query results found".format(res_counter))
        return res_dict

    def post_json(self, this_data):
        # Post a data set to the elasticsearch database. If the database already has an entry with this ID, the old
        # entry will be overwritten.

        # The field "tournament" can be given as JSON with a name and an ID. Also, just a string can be given, which
        # then will be interpreted as the tournament name.
        if type(this_data['data']['tournament']) == str:
            this_name = this_data['data']['tournament']
            this_data['data']['tournament'] = dict()
            this_data['data']['tournament']['id'] = None
            this_data['data']['tournament']['name'] = this_name

        # While there are IDs that are stings, the numeric ID values have to be converted to strings as well.
        this_data['data']['id'] = str(this_data['data']['id'])

        # Create the new document that will be saved to the database.
        game_record = self.Gamerecord(meta={'id': str(this_data['data']['id'])})

        # Fill the data fields of the document.
        game_record.source = this_data['source']
        game_record.id = this_data['data']['id']
        game_record.url = this_data['data']['url']
        game_record.state = this_data['data']['state']
        game_record.bestof = this_data['data']['bestof']
        game_record.title = this_data['data']['title']
        # Add start date as datetime from the format yyyy-mm-dd HH:MM:SS.
        game_record.date_start_text = parse_time(this_data['data']['date_start_text'])
        # Add the nested fields.
        game_record.set_tournament(this_data['data']['tournament'])
        for this_scores_data in this_data['data']['scores']:
            game_record.add_scores(this_scores_data)

        for this_team_data in this_data['data']['teams']:
            game_record.add_team(this_team_data)
        # Save the document to the database.
        game_record.save()

        self.elastic_logger.info('Document has been saved to the database')

