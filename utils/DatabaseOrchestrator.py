import MySQLdb
import psycopg2
import logging
from DatabaseExceptions import *
from Logger import get_logger

class DatabaseOrchestrator:

    def load(self, host, user, passwd, database, databaseType):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.databaseType = databaseType
        self.logger = get_logger("DatabaseOrchestrator")
        if databaseType == "MySQL":
            self.connectedDB = MySQLdb.connect(host, user, passwd, database)
        elif databaseType == "PostgresSQL":
            self.connectedDB = psycopg2.connect("dbname=\'{}\' user=\'{}\'".format(database, user))
        else:
            #Error occured here, no valid handling for databaseType given
            raise DatabaseTypeError(databaseType)
        self.cursor = self.connectedDB.cursor()
       
    def show_tables(self):
        self.logger.info("Inside show_tables, databaseType: {}".format(self.databaseType))
        if self.databaseType == "MySQL":
            try:
                self.cursor.execute("SHOW TABLES")
            except:
                self.logger.error(logging.exception("MySQL - Select tables error"))
                raise DatabaseCursorError("MySQL - SHOW TABLES error")
        elif self.databaseType == "PostgresSQL":
            try:
                self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")
            except:
                self.logger.error(logging.exception("PostgresSQL - Select tables error"))
                raise DatabaseCursorError("PostgresSQL - Select tables error")
        else:
            raise DatabaseTypeError(self.databaseType)
        
        results = self.cursor.fetchall()
        tableList = [table[0] for table in results]
        return tableList

    def show_databases(self):
        self.logger.info("Inside show_databases, databaseType: {}".format(self.databaseType))
        if self.databaseType == "MySQL":
            self.cursor.execute("SHOW DATABASES")
        elif self.databaseType == "PostgresSQL":
            self.cursor.execute("SELECT * FROM pg_database")
        else:
            raise DatabaseTypeError(self.databaseType)
        
        results = self.cursor.fetchall()
        databaseList = [database[0] for database in results]
        return databaseList

    def select_database(self, database):
        self.logger.info("Inside select_database, database: {}".format(database))
        if self.databaseType == "MySQL":
            try:
                self.cursor.execute("USE " + database)
                self.database = database
                return "Successfully selected database"
            except:
                self.logger.error(logging.exception("MySQL - Select database error"))
                raise DatabaseError(self.database)
        elif self.databaseType == "PostgresSQL":
            try:
                self.database = database
                self.connectedDB = psycopg2.connect("dbname=\'{}\' user=\'{}\'".format(database, self.user))
                self.cursor = self.connectedDB.cursor()
                return "Successfully selected database"
            except:
                self.logger.error(logging.exception("PostgresSQL - Select database error"))
                raise DatabaseError(self.database)
        else:
            raise DatabaseTypeError(self.databaseType)

    def query_database(self, query):
        self.logger.info("Inside query_database, query: {}".format(query))
        results = []
        try:
            self.cursor.execute(query)
            
            for tupleResult in self.cursor.fetchall():
                results.append(tupleResult)
        except:
            self.logger.error(logging.exception("MySQL&PostgresSQL - Query database error"))
            raise DatabaseCursorError("Database query failed")
        return results

    def get_table_schema(self, table):
        self.logger.info("Inside get_table_schema, table: {}".format(table))
        tableSchema = []
        if self.databaseType == "MySQL":
            try:
                self.cursor.execute("DESCRIBE " + table)
                for column in self.cursor.fetchall():
                    tableSchema.append(column[:2])
            except:
                self.logger.error(logging.exception("MySQL - Get table schema error"))
                raise DatabaseCursorError("MySQL - Get table schema error")
        if self.databaseType == "PostgresSQL":
            try:
                self.cursor.execute("SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = \'{}\'".format(table))
                for column in self.cursor.fetchall():
                    tableSchema.append(column[:3])
            except:
                self.logger.error(logging.exception("PostgresSQL - Get table schema error"))
                raise DatabaseCursorError("PostgresSQL - Get table schema error")
        return tableSchema

    def get_table_for_viewing(self, table):
        self.logger.info("Inside get_table_for_viewing, table: {}".format(table))
        printableTable = []

        printableTable.append(self.get_table_schema(table))
        printableTable.append(self.query_database("Select * from " + table))
        return printableTable

    def create_database(self, results):
        pass
        self.logger.info("Inside create_database, databaseType: {}".format(self.databaseType))
        if self.databaseType == "MySQL":
            try:
                self.cursor.execute("CREATE DATABASE " + results) #Create a new database in MySQL server
                return results
            except:
                return "ERROR! Check if duplicate name or spaces"
        elif self.databaseType == "PostgresSQL":
            try:
                self.cursor.execute("createdb " + results) #Create a new database in MySQL server
                return results
            except:
                return "ERROR! Check if duplicate name or spaces"
