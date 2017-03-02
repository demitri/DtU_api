#!/usr/bin/python

import numpy as np

import flask
from flask import request, make_response, current_app

from . import valueFromRequest, make_json_response
from ..database_support import APIDB, database_cursor


api_histogram = flask.Blueprint("api_histogram", __name__)

@api_histogram.route("/histogram", methods=['GET'])
def histogram():
	'''

	Parameters:

		attribute (string) : column name
		range (float, float) : range of values
		n_bins (integer) [optional] : number of bins

	'''

	attribute = valueFromRequest(key="attribute", request=request, asList=False)
	range = valueFromRequest(key="range", request=request, asList=True)
	n_bin = valueFromRequest(key="n_bin", request=request, asList=False)

	apidb = APIDB()
	pool = apidb.pool()
	with database_cursor(pool) as cursor:

		print(int(n_bin), range)

		query = "select * from pg_hist_1d('select {0} from kic', ARRAY[{1}], ARRAY[{2}], ARRAY[{3}]);".format(attribute, n_bin, range[0], range[1])
		print(query)
		cursor.execute(query)

		values = np.zeros(int(n_bin))

		# Only non-zero entries are returned
		for row in cursor.fetchall():
			print(row)
			bin_id, count = row
			values[bin_id] = count

	return make_json_response(values.tolist())
