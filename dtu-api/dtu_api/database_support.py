#!/usr/bin/python

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from flask import current_app as app

#from database_support import SDSSAPIDB

class APIDB(object):
	
	def __init__(self):

		#self.config = ConfigParser.ConfigParser()
		#self.config.read(sdss.configuration_file)

		self.pools = {}
		
	def pool(self, release):
		''' Return the pool of database connections for the database connected to the release specified. '''
		
		release = release.lower()

		if release not in sdss.availableReleases() + ["spectradb"]:
			api_error = SDSSAPIError(type=ErrorInvalidParameterValue,
									 detail="An unknown release was specified ('{0}').".format(release))
			raise SDSSAPIException("API error: {0}".format(api_error.detail), apiError=api_error)
		
		# -----------------------------------
		# Database connection setup & methods
		# -----------------------------------
		# Ref: http://initd.org/psycopg/docs/module.html
		# Ref: http://packages.python.org/psycopg2/pool.html#module-psycopg2.pool
		# dsn = data source name

		try:
			return self.pools[release]
		except KeyError:

			if release in ["dr8", "dr9", "dr10", "dr11", "spectradb"]:
				self.pools[release] = ThreadedConnectionPool(minconn=1,
															 maxconn=10,
															 dsn=self.databaseDSN(release))
			else:
				app.logger.debug("An release that we expect to be available ('{0}') is not handled in {1}!!".format(release, __file__))
				return None
		
		return self.pools[release]

	def databaseDSN(self, release=sdss.currentRelease(), uri=False):
		'''
		Return the PostgreSQL DSN string for the specified release.
		If no release is specified, the current release is used.
		
		DSN format reference: http://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING
		
		Keywords recognized in connection string are here:
		http://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS
		
		@param uri Return as an RFC 3986 URI, available only from PostgreSQL 9.2 (see link above).
		'''
	 	if release not in sdss.availableReleases():
 			error = SDSSAPIError(type = ErrorInvalidParameterValue,
 								 detail = "The release specified is not known or available.")
 			raise SDSSAPIException("API error", apiError=api_error)
 		
 		# default values here
 		db_info = {"port" : 5432}
 		
 		# This could be cleaned up a bit to handle unspecified keys or to read values
 		# (e.g. password) from the envirnment or pgpass file.
 		
 		if release == 'dr8':
			# database connection strings
			
			try:
				db_info["database"] = app.config["DR8DB_DATABASE"]
				db_info["host"] = app.config["DR8DB_HOST"]
				db_info["user"] = app.config["DR8DB_USER"]
				db_info["password"] = app.config["DR8DB_PASSWORD"]
				db_info["port"] = app.config["DR8DB_PORT"]
			except KeyError:
				print_error("ERROR: an expected key in the server configuration "
					   		"file was not found (dr8db connection parameter).")

 		elif release == 'dr9':
			try:
				#print(app.config.keys())
				db_info["database"] = app.config["DR9DB_DATABASE"]
				db_info["host"] = app.config["DR9DB_HOST"]
				db_info["user"] = app.config["DR9DB_USER"]
				db_info["password"] = app.config["DR9DB_PASSWORD"]
				db_info["port"] = app.config["DR9DB_PORT"]
			except KeyError:
				print_error("ERROR: an expected key in the server configuration "
					   		"file was not found (dr9db connection parameter).")

		elif release == 'dr10':
			try:
				db_info["database"] = app.config["DR10DB_DATABASE"]
				db_info["host"] = app.config["DR10DB_HOST"]
				db_info["user"] = app.config["DR10DB_USER"]
				db_info["password"] = app.config["DR10DB_PASSWORD"]
				db_info["port"] = app.config["DR10DB_PORT"]
			except KeyError:
				print_error("ERROR: an expected key in the server configuration "
					   		"file was not found (dr10db connection parameter).")

		elif release == "spectradb":
			try:
				db_info["database"] = app.config["SPECTRADB_DATABASE"]
				db_info["host"] = app.config["SPECTRADB_HOST"]
				db_info["user"] = app.config["SPECTRADB_USER"]
				db_info["password"] = app.config["SPECTRADB_PASSWORD"]
				db_info["port"] = app.config["SPECTRADB_PORT"]
			except KeyError:
				print_error("ERROR: an expected key in the server configuration "
					   		"file was not found (spectra connection parameter).")

		else:
			app.logger.debug("An release that we expect to be available "
							"('{0}') is not handled in {1}!!".format(release, __file__))
			return None
		
		if uri:
			# only usable with PostgreSQL 9.2+
			dsn = "postgresql://{user}:{password}@{host}:{port}/{database}".format(**db_info)
		else: 
			dsn = "host={host} port={port} user={user} password={password} dbname={database}".format(**db_info)

		#print_info("DSN = {0}".format(dsn))
		return dsn

