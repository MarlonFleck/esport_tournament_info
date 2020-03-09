"""
FLASK API SERVER
Here the flask server is run that provides an API for the user to query the elasticsearch database.
"""
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from http import HTTPStatus
from elastic import elastic_server
from settings import filter_keywords_must, logger_name
import logging


def get_server():
    # Get the logger.
    logger_name_server = logger_name + '.api_server'
    server_logger = logging.getLogger(logger_name_server)

    app = Flask(__name__)
    api = Api(app)

    # Setup a parser that allows argument inputs for title, tournament, state, start date and end date. These arguments
    # will be used to filter queries by. Arguments that are not defined won't effect the search result.
    parser_filter = reqparse.RequestParser()
    for this_filter_keyword in filter_keywords_must:
        parser_filter.add_argument(this_filter_keyword)

    parser_filter.add_argument('tournament')
    parser_filter.add_argument('date_start_gte')
    parser_filter.add_argument('date_start_lte')

    # Define route to get a list of matches, that can be filtered by
    # "date_start_gte", "date_start_lte", "tournament", "title" and "state"
    class GetMatches(Resource):
        def get(self):
            server_logger.info('GET request received')
            try:
                args = parser_filter.parse_args()
                result = elastic_server.get_filtered(args)
                return jsonify(result)
            except Exception as e:
                server_logger.error(e)
                # If there was an Exception in getting the query results, show a bad request and log the error.
                return HTTPStatus.BAD_REQUEST

    api.add_resource(GetMatches, '/get_matches')

    server_logger.info("Flask API server running - http://localhost:5000/get_matches")

    return app


if __name__ == '__main__':
    server_app = get_server()
    server_app.run(debug=True)
