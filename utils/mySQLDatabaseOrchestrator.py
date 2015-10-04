import MySQLdb

class MySQLDatabaseOrchestrator:

    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.connectedDB = MySQLdb.connect(host, user, passwd, database)
        self.cursor = self.connectedDB.cursor()
       
    def show_tables(self):
        tableList = []
        try:
            self.cursor.execute("SHOW TABLES")
            for (table,) in self.cursor.fetchall():
                tableList.append(table)
        except:
            tableList.append("ERROR")
        return tableList

    def show_databases(self):
        self.cursor.execute("SHOW DATABASES");
        databaseList = []
        for (database,) in self.cursor.fetchall():
            databaseList.append(database)
        return databaseList

    def select_database(self, database):
        try:
            self.cursor.execute("USE " + database)
            self.database = database
            return "Successfully selected database"
        except:
            return "Failed to select database"

    def query_database(self, query):
        results = []
        try:
            self.cursor.execute(query)
            
            for tupleResult in self.cursor.fetchall():
                results.append(tupleResult)
        except:
            results.append("ERROR")
        return results

    def get_table_schema(self, table):
        tableSchema = []
        try:
            self.cursor.execute("DESCRIBE " + table)
            for column in self.cursor.fetchall():
                tableSchema.append(column[:2])
        except:
            tableSchema.append("ERROR")
        return tableSchema

    def get_table_for_viewing(self, table):
        printableTable = []

        printableTable.append(self.get_table_schema(table))
        printableTable.append(self.query_database("Select * from " + table))
        return printableTable
