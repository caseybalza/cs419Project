from ..DatabaseOrchestrator import DatabaseOrchestrator, MySQLdb, psycopg2, os
from ..DatabaseExceptions import *
import pytest

class dummy_bad_cursor:
    results = []

    def __call__(self):
        return self

    def execute(self, query):
        raise DatabaseCursorError("Cursor error")
    
    def fetchall(self):
        return self.results

class dummy_cursor:
    results = []
    description = [('a','b','c'),('d','e','f'),('g','h','i')]

    def __call__(self):
        return self

    def execute(self, query):
        if query == "SHOW DATABASES" or query == "SELECT * FROM pg_database":
            self.results = ['database1', 'database2', 'database3']
        elif query == "SHOW TABLES" or query == "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'":
            self.results = ['table1', 'table2', 'table3']
        elif query[:8] == "DESCRIBE" or query[:18] == "SELECT column_name":
            self.results = [('1','2','3'),('4','5','6'),('7','8','9')]
        elif query[:8] == "SELECT *":
            self.results = [('9','8','7'),('6','5','4'),('3','2','1')]
        else:
            return

    def fetchall(self):
        return self.results

class dummy_MySQLdb_connection:
    def __call__(self, host, user, passwd, database):
        if host != "localhost" or user != "root" or passwd != "password":
            raise DatabaseConnectError
        return self

    def cursor(self):
        return dummy_cursor()

    def commit(self):
        return

class dummy_psycopg_connection:
    def __call__(self, login_info):
        if login_info != "dbname=\'\' user=\'ubuntu\'":
            raise DatabaseConnectError
        return self

    def cursor(self):
        return dummy_cursor()

class dummy_system:
    def __call__(self, call):
        return

class dummy_bad_system:
    def __call__(self, call):
        raise Exception

class TestMySQLDatabaseOrchestrator:
    dbo = DatabaseOrchestrator()
    MySQLdb.connect = dummy_MySQLdb_connection()
    os.system = dummy_system()

    def test_load_MySQL(self):
        self.dbo.load('localhost', 'root', 'password', '', 'MySQL')

    def test_load_invalid_databaseType(self):
        with pytest.raises(DatabaseTypeError):
            self.dbo.load('localhost', 'root', 'password', '', 'MicrosoftSQL')

    def test_load_invalid_MySQL_Login(self):
        with pytest.raises(DatabaseConnectError):
            self.dbo.load('localhost', 'root', 'not_the_password', '', 'MySQL')

    def test_show_databases_MySQL(self):
        self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
        assert type(self.dbo.show_databases()) is list

    def test_show_databases_invalid_databaseType(self):
        with pytest.raises(DatabaseTypeError):
            try:
                self.dbo.load('localhost', 'root', 'password', '', 'MicrosoftSQL')
            except:
                pass

            self.dbo.show_databases()

    def test_show_databases_MySQL_no_databases(self):
        self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
        assert type(self.dbo.show_databases()) is list

    def test_show_tables(self):
        self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
        self.dbo.select_database('RandomDatabase')
        assert type(self.dbo.show_tables()) is list

    def test_show_tables_failure(self):
        with pytest.raises(DatabaseCursorError):
            self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
            self.dbo.select_database('RandomDatabase')
            self.dbo.cursor = dummy_bad_cursor()
            self.dbo.show_tables()
    
    def test_show_tables_invalid_databaseType(self):
        with pytest.raises(DatabaseTypeError):
            try:
                self.dbo.load('localhost', 'root', 'password', '', 'MicrosoftSQL')
            except:
                pass
            self.dbo.select_database('RandomDatabase')
            self.dbo.show_tables()

    def test_query_database(self):
        self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
        self.dbo.select_database('RandomDatabase')
        assert type(self.dbo.query_database('RandomQuery')) is list

    def test_query_database_failure(self):
        with pytest.raises(DatabaseCursorError):
            self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
            self.dbo.select_database('RandomDatabase')
            self.dbo.cursor = dummy_bad_cursor()
            self.dbo.query_database('RandomQuery')

    def test_custom_query(self):
        self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
        self.dbo.select_database('RandomDatabase')
        assert type(self.dbo.custom_query('SELECT * FROM RandomTable')) is list
        assert type(self.dbo.custom_query('SELECT * FROM RandomTable')[0]) is list
        assert type(self.dbo.custom_query('SELECT * FROM RandomTable')[1]) is list
        assert len(self.dbo.custom_query('INVALID QUERY')[0]) == 0
        assert len(self.dbo.custom_query('INVALID QUERY')[1]) == 0

    def test_custom_query_failure(self):
        with pytest.raises(DatabaseCursorError):
            self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
            self.dbo.select_database('RandomDatabase')
            self.dbo.cursor = dummy_bad_cursor()
            self.dbo.custom_query('SELECT * FROM RandomTable')

    def test_get_table_schema(self):
        self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
        self.dbo.select_database('RandomDatabase')
        assert type(self.dbo.get_table_schema('RandomTable')) is list
        assert type(self.dbo.get_table_schema('RandomTable')[0]) is tuple

    def test_get_table_schema_failure(self):
        with pytest.raises(DatabaseCursorError):
            self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
            self.dbo.select_database('RandomDatabase')
            self.dbo.cursor = dummy_bad_cursor()
            self.dbo.get_table_schema('RandomTable')
    
    def test_get_table_for_viewing(self):
        self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
        self.dbo.select_database('RandomDatabase')
        assert type(self.dbo.get_table_for_viewing('RandomTable')) is list
        assert type(self.dbo.get_table_for_viewing('RandomTable')[0]) is list
        assert type(self.dbo.get_table_for_viewing('RandomTable')[1]) is list
        assert type(self.dbo.get_table_for_viewing('RandomTable')[0][0]) is tuple
        assert type(self.dbo.get_table_for_viewing('RandomTable')[1][0]) is tuple

    def test_get_table_for_viewing_failure(self):
        with pytest.raises(DatabaseCursorError):
            self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
            self.dbo.select_database('RandomDatabase')
            self.dbo.cursor = dummy_bad_cursor()
            self.dbo.get_table_for_viewing('RandomTable')

    def test_create_database(self):
        self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
        self.dbo.create_database('NewDatabase')

    def test_create_database_failure(self):
        with pytest.raises(DatabaseCursorError):
            self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
            self.dbo.cursor = dummy_bad_cursor()
            self.dbo.create_database('NewDatabase')

    def test_delete_database(self):
        self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
        self.dbo.delete_database('RandomDatabase')

    def test_delete_database_failure(self):
        with pytest.raises(DatabaseCursorError):
            self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
            self.dbo.cursor = dummy_bad_cursor()
            self.dbo.delete_database('RandomDatabase')

    def test_export_database(self):
        self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
        self.dbo.export_database('RandomDatabase')

    def test_export_database_failure(self):
        with pytest.raises(DatabaseCursorError):
            self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
            os.system = dummy_bad_system()
            self.dbo.export_database('RandomDatabase')

    def test_import_database(self):
        self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
        os.system = dummy_system()
        self.dbo.import_database('RandomDatabase')

    def test_import_database_failure(self):
        with pytest.raises(DatabaseCursorError):
            self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
            os.system = dummy_bad_system()
            self.dbo.import_database('RandomDatabase')

    def test_perform_bulk_operations(self):
        self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
        self.dbo.select_database('RandomDatabase')
        self.dbo.perform_bulk_operations(['INSERT SOMETHING INTO SOMETHING', 'UPDATE SOMETHING WHERE SOMETHING IS SOMETHING'])

    def test_perform_bulk_operations_failure(self):
        with pytest.raises(DatabaseCursorError):
            self.dbo.load('localhost', 'root', 'password', '', 'MySQL')
            self.dbo.select_database('RandomDatabase')
            self.dbo.cursor = dummy_bad_cursor()
            self.dbo.perform_bulk_operations(['INSERT SOMETHING INTO SOMETHING', 'UPDATE SOMETHING WHERE SOMETHING IS SOMETHING'])
        
class TestPostgresSQLDatabaseOrchestrator:
    dbo = DatabaseOrchestrator()
    psycopg2.connect = dummy_psycopg_connection()

    def test_load_PostgresSQL(self):
        self.dbo.load('localhost', 'ubuntu', 'password', '', 'PostgresSQL')

    def test_load_invalid_databaseType(self):
        with pytest.raises(DatabaseTypeError):
            self.dbo.load('localhost', 'ubuntu', 'password', '', 'MicrosoftSQL')

    def test_show_databases_PostgresSQL(self):
        self.dbo.load('localhost', 'ubuntu', 'password', '', 'PostgresSQL')
        assert type(self.dbo.show_databases()) is list

    def test_show_databases_invalid_databaseType(self):
        with pytest.raises(DatabaseTypeError):
            try:
                self.dbo.load('localhost', 'ubuntu', 'password', '', 'MicrosoftSQL')
            except:
                pass
            
            self.dbo.show_databases()

    def test_show_databases_PostgresSQL_no_databases(self):
        self.dbo.load('localhost', 'ubuntu', 'password', '', 'PostgresSQL')
        assert type(self.dbo.show_databases()) is list
