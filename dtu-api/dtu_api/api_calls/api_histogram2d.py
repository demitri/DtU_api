#!/usr/bin/python

import numpy as np

import flask
from flask_restful import reqparse
from flask import request, make_response, current_app

from . import valueFromRequest, make_json_response
from ..database_support import APIDB, database_cursor
from .utils import selection_to_where

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

	x_attribute = valueFromRequest(key="x_attribute", request=request)
	y_attribute = valueFromRequest(key="y_attribute", request=request)
	x_range = valueFromRequest(key="x_range", request=request, asList=True)
	y_range = valueFromRequest(key="y_range", request=request, asList=True)
	x_n_bins = valueFromRequest(key="x_n_bins", request=request)
	y_n_bins = valueFromRequest(key="y_n_bins", request=request)

	selection = valueFromRequest(key="selection", request=request, asList=False)
	where = selection_to_where(selection)

	apidb = APIDB()
	pool = apidb.pool()
	with database_cursor(pool) as cursor:

		query = "select * from pg_hist_2d('select {0},{1} from kic {2} LIMIT 1000000', ARRAY[{3},{4}], ARRAY[{5},{6}], ARRAY[{7},{8}]);".format(x_attribute, y_attribute, where, x_n_bins, y_n_bins, x_range[0], y_range[0], x_range[1], y_range[1])
		cursor.execute(query)

		values = np.zeros((int(y_n_bins), int(x_n_bins)))

		# Only non-zero entries are returned
		for row in cursor.fetchall():
			x_id, y_id, count = row
			values[y_id, x_id] = count

	return make_json_response(values.tolist())
