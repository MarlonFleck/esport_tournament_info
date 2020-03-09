"""
DEFINITION OF THE DOCUMENT DATA ENTRIES AND TYPES FOR GAME DATA THAT WILL BE STORED IN ELASTICSEARCH
"""
from elasticsearch_dsl import Document, Integer, Date, Text, InnerDoc, Nested, Boolean
from settings import es_index
from elasticsearch_dsl.connections import connections
from settings import es_host_add, es_port

""" Definition of nested data types in the document """
class Tournament(InnerDoc):
    name = Text()
    id = Integer()


class Teams(InnerDoc):
    name = Text()
    id = Integer()


class Scores(InnerDoc):
    team = Integer()
    score = Integer()
    winner = Boolean()


""" Definition of document entries and types """
class Gamerecord(Document):
    # Setup all the entries of a game record document.
    source = Text()
    id = Text()
    url = Text()
    state = Integer()
    teams = Nested(Teams)
    bestof = Integer()
    scores = Nested(Scores)
    tournament = Nested(Tournament)
    date_start_text = Date()
    title = Text()

    def set_tournament(self, kwargs):
        self.tournament = Tournament(**kwargs)

    def add_team(self, kwargs):
        self.teams.append(Teams(**kwargs))

    def add_scores(self, kwargs):
        self.scores.append(Scores(**kwargs))

    class Index:
        name = es_index
        settings = {
          "number_of_shards": 1,
        }

    def save(self, **kwargs):
        return super(Gamerecord, self).save(**kwargs)

