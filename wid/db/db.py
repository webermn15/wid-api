import psycopg2


class Database(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            # replace hardcoded db details with v a r i a b l e s
            config = "dbname=nintendo user=michael"

            try:
                print("Attempting to connect to PostgreSQL...")
                connection = Database._instance.connection = psycopg2.connect(config)
                cursor = Database._instance.cursor = connection.cursor()
                cursor.execute("SELECT VERSION();")
                db_version = cursor.fetchone()

            except Exception as error:
                print("Error connecting to the database... {}".format(error))
                Database._instance = None

            else:
                print("Connection to database established. \n{}".format(db_version))

        return cls._instance

    def __init__(self):
        self.connection = self._instance.connection
        self.cursor = self._instance.cursor

    def get_first_result(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()

        except Exception as error:
            print('error running this query:\n{} error message:\n{}'.format(query, error))
            return None

        else:
            return result

    def __del__(self):
        self.cursor.close()
        self.connection.close()
