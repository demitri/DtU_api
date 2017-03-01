#!/usr/bin/python

import numpy as np

import flask
from flask import request, make_response, current_app

from . import valueFromRequest, make_json_response

api_histogram = flask.Blueprint("api_histogram", __name__)

@api_histogram.route("/histogram", methods=['GET'])
def histogram():
	'''
	
	Parameters:
		
		attribute (string) : column name
		range (float, float) : range of values
		n_bins (integer) [optional] : number of bins
	
	'''
	
	return_array = []	
	
	attribute = valueFromRequest(key="attribute", request=request)
	range = valueFromRequest(key="range", request=request, asList=True)
	n_bin = valueFromRequest(key="n_bin", request=request)
	
	return_array.append(attribute)
	return_array.append(range)
	return_array.append(n_bin)
			
	return make_json_response(np.random.rand(500).tolist())
	
