#!/usr/bin/python

import numpy as np

import flask
from flask_restful import reqparse
from flask import request, make_response, current_app

from . import valueFromRequest, make_json_response
from ..database_support import APIDB, database_cursor

api_db_test = flask.Blueprint("api_db_test", __name__)

@api_db_test.route("/db_test", methods=['GET'])
def db_test():
	'''
	
	'''

	apidb = APIDB()
	pool = apidb.pool()
	with database_cursor(pool) as cursor:
		query = "SELECT * FROM kic LIMIT 2"
		cursor.execute(query)
	
		results = list()
		for row in cursor.fetchone():
			results.append(row)
	
	return make_json_response(results)
	
