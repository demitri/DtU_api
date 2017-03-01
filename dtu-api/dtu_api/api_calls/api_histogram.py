#!/usr/bin/python

import flask
from flask import request, make_response, current_app

from . import make_json_response

api_histogram = flask.Blueprint("api_histogram", __name__)

@api_histogram.route("/histogram", methods=['GET'])
def histogram():
	'''
	
	'''
	test_dict = {"A":"value"}
	
	return make_json_response(test_dict)
	
