import MySQLdb
import psycopg2
import logging
from DatabaseExceptions import *
from Logger import get_logger
import os


class DatabaseOrchestrator:

    def load(self, host, user, passwd, database, databaseType):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.databaseType = databaseType
        self.logger = get_logger("DatabaseOrchestrator")
        if databaseType == "MySQL":
            try:
                self.connectedDB = MySQLdb.connect(host, user, passwd, database)
            except:
                self.logger.error(logging.exception("MySQL - Login failure"))
                raise DatabaseConnectError("MySQL - Login failure")

        elif databaseType == "PostgresSQL":
            try:
                self.connectedDB = psycopg2.connect("dbname=\'{}\' user=\'{}\'".format(database, user))
            except:
                self.logger.error(logging.exception("PostgresSQL - Login failure"))
                raise DatabaseConnectError("PostgresSQL - Login failure")
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

    def custom_query(self, query):
        self.logger.info("Inside custom_query, query: {}".format(query))
        results = [[],[]]
        if query[:6] != "SELECT":
            return results

        try:

            self.cursor.execute(query)
            for tupleResult in self.cursor.fetchall():
                results[1].append(tupleResult)
        except:
            self.logger.error(logging.exception("MySQL&PostgresSQL - Custom query error"))
            raise DatabaseCursorError("Database query failed")

        for column in self.cursor.description:
            results[0].append(column[:2])

        #results.insert(0, self.cursor.description)
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
        self.logger.info("Inside create_database, databaseType: {}".format(self.databaseType))
        if self.databaseType == "MySQL":
            try:
                self.cursor.execute("CREATE DATABASE " + results) #Create a new database in MySQL server
            except:
                self.logger.error(logging.exception("MySQL - Create database error"))
                raise DatabaseCursorError("MySQL - Create database error")
        elif self.databaseType == "PostgresSQL":
            try:
                con = psycopg2.connect(dbname='postgres', user=self.user, host=self.host, password=self.passwd)
                con.autocommit = True
                cur = con.cursor()
                cur.execute("CREATE DATABASE " + results)
                con.close()
            except:
                self.logger.error(logging.exception("PostgresSQL - Create database error"))
                raise DatabaseCursorError("PostgresSQL - Create database error")

    def delete_database(self, results):
        self.logger.info("Inside delete_database, databaseType: {}".format(self.databaseType))
        if self.databaseType == "MySQL":
            try:
                self.cursor.execute("DROP DATABASE " + results) #Delete database in MySQL server
            except:
                self.logger.error(logging.exception("MySQL - Delete database error"))
                raise DatabaseCursorError("MySQL - Delete database error")
        elif self.databaseType == "PostgresSQL":
            try:
                self.connectedDB.close()#Must close previous connections in order to delete active db
                con = psycopg2.connect(dbname='postgres', user=self.user, host=self.host, password=self.passwd)
                con.autocommit = True
                cur = con.cursor()
                cur.execute("DROP DATABASE " + results)
                con.close()
            except:
                self.logger.error(logging.exception("PostgresSQL - Delete database error"))
                raise DatabaseCursorError("PostgresSQL - Delete database error")

    def export_database(self, results):
        self.logger.info("Inside export_database, databaseType: {}".format(self.databaseType))
        if self.databaseType == "MySQL":
            try:
                #Export database in MySQL server to databases directory
                 os.system('mysqldump -u root --password=' + self.passwd + ' --databases ' + results + ' > databases/' + results + '.sql')
            except:
                self.logger.error(logging.exception("MySQL - Export database error"))
                raise DatabaseCursorError("MySQL - Export database error")
        elif self.databaseType == "PostgresSQL":
            try:
                 #Export database in PostgreSQL server to databases directory
                 os.system('pg_dump -C -U' + self.user + ' ' + results + ' > databases/' + results + '.sql')
            except:
                self.logger.error(logging.exception("PostgresSQL - Export database error"))
                raise DatabaseCursorError("PostgresSQL - Export database error")

    def import_database(self, results):
        self.logger.info("Inside import_database, databaseType: {}".format(self.databaseType))
        if self.databaseType == "MySQL":
            try:
                #Import database to MySQL server from databases directory
                os.system('mysql -u root -p' + self.passwd + ' < databases/' + results + '.sql')
            except:
                self.logger.error(logging.exception("MySQL - Import database error"))
                raise DatabaseCursorError("MySQL - Import database error")
        elif self.databaseType == "PostgresSQL":
            try:
                 #Must create db first.
                 #Import database to PostgreSQL server from databases directory
                 con = psycopg2.connect(dbname='postgres', user=self.user, host=self.host, password=self.passwd)
                 con.autocommit = True
                 cur = con.cursor()
                 cur.execute("CREATE DATABASE " + results)
                 os.system('psql -U' + self.user + ' ' + results + ' < databases/' + results + '.sql > /dev/null 2>&1')
                 con.close()
            except:
                self.logger.error(logging.exception("PostgresSQL - Import database error"))
                raise DatabaseCursorError("PostgresSQL - Import database error")
    
    def perform_bulk_operations(self, operations):
        if self.databaseType == "MySQL":
            self.cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        for operation in operations:
            try:
                self.cursor.execute(operation)
            except Exception, e:
                self.logger.error("Underlying operation exception: {}".format(e))
                self.logger.error("Operation: {} failed".format(operation))
                raise DatabaseCursorError("Cursor Operation failed")
        if self.databaseType == "MySQL":
            self.cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        self.connectedDB.commit()
