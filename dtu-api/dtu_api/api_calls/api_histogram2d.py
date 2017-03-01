#!/usr/bin/python

import numpy as np

import flask
from flask_restful import reqparse
from flask import request, make_response, current_app

from . import valueFromRequest, make_json_response

api_histogram_2d = flask.Blueprint("api_histogram_2d", __name__)

@api_histogram_2d.route("/histogram_2d", methods=['GET'])
def histogram2d():
	'''
	
	Parameters:
		
		x_attribute (string) : column name
		y_attribute (string) : column name
		x_range (float, float) : range of values
		y_range (float, float) : range of values
		x_n_bins (integer) [optional] : number of bins, x axis
		x_n_bins (integer) [optional] : number of bins, y axis
	
	'''
	
	return_array = []	
	
	attribute = valueFromRequest(key="attribute", request=request)
	x_range = valueFromRequest(key="x_range", request=request, asList=True)
	y_range = valueFromRequest(key="y_range", request=request, asList=True)
	x_n_bins = valueFromRequest(key="x_n_bins", request=request)
	y_n_bins = valueFromRequest(key="y_n_bins", request=request)
		
	query = "SELECT * FROM kic LIMIT 2"
	
	return make_json_response(np.random.rand(500,500).tolist())
	



