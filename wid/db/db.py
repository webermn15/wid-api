import psycopg2


class Database(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            # replace hardcoded db details with e n v  v a r i a b l e s
            config = "dbname=widdev user=michael"

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

    def get_activity(self, id):
        try:
            self.cursor.execute("SELECT * FROM activities WHERE id = %s", (id))
            result = self.cursor.fetchone()

        except Exception as error:
            print('error returning activity with id:\n{} error message:\n{}'.format(id, error))
            return None

        else:
            return result

    def create_activity(self, name, description):
        try:
            self.cursor.execute("INSERT INTO activities (name, description) VALUES (%s, %s)", (name, description))
            self.connection.commit()

        except Exception as error:
            print("error inserting record in table:\n{}".format(error))
            return None

        else:
            self.cursor.execute("SELECT * FROM activities")
            results = self.cursor.fetchall()
            return results

    def __del__(self):
        self.cursor.close()
        self.connection.close()
