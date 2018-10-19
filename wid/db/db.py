import psycopg2
import bcrypt


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

    def authenticate_user(self, username, password):
        return self._compare_hash(username, password)

    def _compare_hash(self, username, password):
        db_hash = self._get_stored_hash(username)
        new_hash = self._generate_hash(password, self._get_stored_salt(username))
        return db_hash == new_hash

    def _generate_hash(self, password, salt):
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def _get_stored_hash(self, username):
        try:
            self.cursor.execute("SELECT password FROM users WHERE username=%s;", (username,))
            stored_hash = self.cursor.fetchone()[0].tobytes()

        except Exception as error:
            print('failed to get stored hashed password.\n error message:\n{}'.format(error))

        else:
            return stored_hash

    def _get_stored_salt(self, username):
        try:
            self.cursor.execute("SELECT salt FROM users WHERE username=%s;", (username,))
            stored_salt = self.cursor.fetchone()[0].tobytes()

        except Exception as error:
            print('failed to get stored salt.\n error message:\n{}'.format(error))

        else:
            return stored_salt

    def create_user(self, username, password):
        salt = bcrypt.gensalt(12)
        pw = password.encode('utf-8')
        hashed = self._hash_password(pw, bytes(salt))

        try:
            self.cursor.execute("INSERT INTO users (username, password, salt) VALUES (%s, %s, %s);", (username, hashed, salt,))
            self.connection.commit()

        except Exception as error:
            print('error creating user in psql.\n error message:\n{}'.format(error))
            return None

        else:
            return True

    def _hash_password(self, password, salt):
        hashed_pw = bcrypt.hashpw(password, salt)
        return hashed_pw

    def get_activity(self, id):
        try:
            self.cursor.execute("SELECT * FROM activities WHERE id = %s;", (id,))
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
