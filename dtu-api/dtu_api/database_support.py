#!/usr/bin/python

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from flask import current_app as app
from contextlib import contextmanager

class APIDB(object):
	
	def __init__(self):

		#self.config = ConfigParser.ConfigParser()
		#self.config.read(sdss.configuration_file)

		#self.pools = {} # incase multiple pools/db connections are needed
		self._pool = None
		
	def pool(self):
		''' Return the pool of database connections. '''
		
		# -----------------------------------
		# Database connection setup & methods
		# -----------------------------------
		# Ref: http://initd.org/psycopg/docs/module.html
		# Ref: http://packages.python.org/psycopg2/pool.html#module-psycopg2.pool
		# dsn = data source name

		if (self._pool == None):
			self._pool = ThreadedConnectionPool(minconn=1,
											   maxconn=10,
											   dsn=self.databaseDSN())
		return self._pool


	def databaseDSN(self, uri=False):
		'''
		Return the PostgreSQL DSN string for the database.
		
		DSN format reference: http://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING
		
		Keywords recognized in connection string are here:
		http://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS
		
		@param uri Return as an RFC 3986 URI, available only from PostgreSQL 9.2+ (see link above).
		'''
 		
		# default values here
		db_info = {"port" : 5432}
		
		# This could be cleaned up a bit to handle unspecified keys or to read values
		# (e.g. password) from the envirnment or pgpass file.
 		
		try:
			db_info["database"] = app.config["DB_DATABASE"]
			db_info["host"] = app.config["DB_HOST"]
			db_info["user"] = app.config["DB_USER"]
			db_info["password"] = app.config["DB_PASSWORD"]
			db_info["port"] = app.config["DB_PORT"]
		except KeyError:
			print_error("ERROR: an expected key in the server configuration file was not found.")

		if uri:
			# only usable with PostgreSQL 9.2+
			dsn = "postgresql://{user}:{password}@{host}:{port}/{database}".format(**db_info)
		else: 
			dsn = "host={host} port={port} user={user} password={password} dbname={database}".format(**db_info)

		#print_info("DSN = {0}".format(dsn))
		return dsn

@contextmanager
def database_cursor(pool, use_dict_cursor=False):
	'''
	This function allows one to use a database connection without having to worry about
	returning it to the pool when we're done with it.
	
	Example usage:
	
	pool = apidb.pool(release=sdss.currentRelease())
	with database_cursor(pool) as cursor:
		# do stuff with cursor, can even return from block
		# will return connection to pool when block is done
	'''
	# --------------------------
	# ON ENTER OF WITH STATEMENT
	# --------------------------
	# perform any setup/initialization here
	dbconnection = pool.getconn()
	if use_dict_cursor:
		cursor = dbconnection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	else:
		cursor = dbconnection.cursor()
	yield cursor
	
	# -------------------------
	# ON EXIT OF WITH STATEMENT
	# -------------------------
	# this gets called on exit of the "with" block, no matter what
	#app.logger.debug("Returning connection to the pool")
	pool.putconn(dbconnection)	

