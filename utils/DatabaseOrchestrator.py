import MySQLdb
import psycopg2
from DatabaseExceptions import *

class DatabaseOrchestrator:

    def __init__(self, host, user, passwd, database, databaseType):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.databaseType = databaseType
        if databaseType == "MySQL":
            self.connectedDB = MySQLdb.connect(host, user, passwd, database)
        elif databaseType == "PostgresSQL":
            self.connectedDB = psycopg2.connect("dbname=\'{}\' user=\'{}\'".format(database, user))
        else:
            #Error occured here, no valid handling for databaseType given
            raise DatabaseTypeError(databaseType)
        self.cursor = self.connectedDB.cursor()
       
    def show_tables(self):
        if self.databaseType == "MySQL":
            try:
                self.cursor.execute("SHOW TABLES")
            except:
                raise DatabaseCursorError("MySQL - SHOW TABLES error")
        elif self.databaseType == "PostgresSQL":
            try:
                self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")
            except:
                raise DatabaseCursorError("PostgresSQL - Select tables error")
        else:
            raise DatabaseTypeError(self.databaseType)
        
        results = self.cursor.fetchall()
        tableList = [table[0] for table in results]
        return tableList

    def show_databases(self):
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
        if self.databaseType == "MySQL":
            try:
                self.cursor.execute("USE " + database)
                self.database = database
                return "Successfully selected database"
            except:
                return "Failed to select database"
        elif self.databaseType == "PostgresSQL":
            try:
                self.database = database
                self.connectedDB = psycopg2.connect("dbname=\'{}\' user=\'{}\'".format(database, self.user))
                self.cursor = self.connectedDB.cursor()
                return "Successfully selected database"
            except:
                return "Failed to select database"
        else:
            raise DatabaseTypeError(self.databaseType)

    def query_database(self, query):
        results = []
        try:
            self.cursor.execute(query)
            
            for tupleResult in self.cursor.fetchall():
                results.append(tupleResult)
        except:
            raise DatabaseCursorError("Database query failed")
        return results

    def get_table_schema(self, table):
        tableSchema = []
        if self.databaseType == "MySQL":
            try:
                self.cursor.execute("DESCRIBE " + table)
                for column in self.cursor.fetchall():
                    tableSchema.append(column[:2])
            except:
                DatabaseCursorError("MySQL - Get table schema error")
        if self.databaseType == "PostgresSQL":
            try:
                self.cursor.execute("SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = \'{}\'".format(table))
                for column in self.cursor.fetchall():
                    tableSchema.append(column[:3])
            except:
                DatabaseCursorError("PostgresSQL - Get table schema error")
        return tableSchema

    def get_table_for_viewing(self, table):
        printableTable = []

        printableTable.append(self.get_table_schema(table))
        printableTable.append(self.query_database("Select * from " + table))
        return printableTable
