import mysql.connector
from mysql.connector import Error
import pandas as pd

import sys
sys.path.insert(0, '/home/apprenant/Documents/simplon_dev/python_sql/lol_api') # Change with your own project path

from src.config import USER, PASSWORD, DB_NAME # Build your own config file

CSV_PATH = '/home/apprenant/Documents/simplon_dev/python_sql/lol_api/Data/dataclear.csv'
df = pd.read_csv(CSV_PATH)
df = df.drop('Unnamed: 0', axis=1)

df['blue_kills_by_timeline'] = df.loc[:,['kill_1', 'kill_2', 'kill_3', 'kill_4', 'kill_5']].sum(axis=1)
df['red_kills_by_timeline'] = df.loc[:,['kill_6', 'kill_7', 'kill_8', 'kill_9', 'kill_10']].sum(axis=1)

cols_to_keep = ['match_ID', 'timeline', 'who_win', 'blue_kills_by_timeline', 'red_kills_by_timeline', 'blue_gold', 'red_gold']
df = df[cols_to_keep]

#print(df.head(42))

class Database:
    connection = None

    def __init__(self, host_name, user_name, user_password ,db_name):
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.db_name = db_name

    def db_connection(self):
        """
        Make the connection with a mysql user, 
        parameters are defined in a config file for security
        """
        try:
            self.connection = mysql.connector.connect(
                host = self.host_name,
                user = self.user_name,
                password = self.user_password,
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")

        return self.connection

    def create_database(self, connection):
        """
        Create a database if it doesn't exist yet
        The db name is retrieved from a config file as well
        """
        query = "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(self.db_name)
        try:
            connection.execute(query)
            print('DB created !!!')
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def disconnect_db(self):
        """
        Close the database connection
        """
        self.connection.close()	# Disconnect
        print('Succesfully disconnected.')


    def fill_database(self, cursor,connection):
        use_query = "USE {}".format(self.db_name)
        table_query = '''
            CREATE TABLE IF NOT EXISTS game (
                match_ID bigint, 
                timeline int, 
                who_win VARCHAR(50), 
                blue_kills_by_timeline int,
                red_kills_by_timeline int,
                blue_gold int,
                red_gold int)
        '''
        try:
            cursor.execute(use_query)
            cursor.execute(table_query)
            for row in df.itertuples():
                print(row)
                cursor.execute(
                    '''
                        INSERT INTO game(
                            match_ID, 
                            timeline, 
                            who_win,
                            blue_kills_by_timeline,
                            red_kills_by_timeline,
                            blue_gold,
                            red_gold
                        )
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                    ''',
                    (
                        row.match_ID,
                        row.timeline,
                        row.who_win,
                        row.blue_kills_by_timeline,
                        row.red_kills_by_timeline,
                        row.blue_gold,
                        row.red_gold
                    )
                )
                connection.commit()
        except mysql.connector.Error as err:
            print("Failed populating the database: {}".format(err))
            exit(1)

#######################################
# OBJECT INSTANCIATION + METHOD CALLS #
#######################################

"""# Instaciation of the database object
db = Database('localhost', USER, PASSWORD, DB_NAME)
# Connection to the db
con = db.db_connection()
cursor = con.cursor()
# Create the database
db.create_database(cursor)
# Fill the database with data
db.fill_database(cursor,con)

db.disconnect_db()
cursor.close()"""
