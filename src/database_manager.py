# This is the file that manages all database related tasks.
# import mysql.connector
import sys
import mariadb
import os
from security import find_hash
import string
import random

class database_manager:
    """class to manage all database related tasks."""

    def __init__(self):
        # initialize some stuff
        # here this thing is not instantly called coz we wont be multithreading the creation of the object,
        # only rather its methods.
        # self.connection_obj = None
        self.user_game_scores = {
            "2048": 0,
            "icy": 0,
            "snake": 0,
            "tetris": 0,
            "space wars": 0,
        }
        self.user_data = {
            "user_name": None,
            "user_email": None,
            "user_pass_hash": None,
            "user_score": 0,
            "user_salt": None,
            "user_games": ["snake", "tetris"]
        }
        self.top_scores = None
        self.cursor = None
        self.games_owned_by_user = ["snake", "tetris"]

    def generate_random_string(self, length):
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))    
        return str(ran)
    
    def connect_and_create_tables(self):
        """forms connection with sql, and returns True.
            or else returns False
        Returns:
            _type_: _description_
        """
        try:
            self.connection = mariadb.connect(
                user="krishnaraj",
                password="mariamaria",
                host="127.0.0.1",
                port=3306,
                database="Puzzlelists",
            )
        except mariadb.Error as ex:
            print(f"An error occurred while connecting to MariaDB: {ex}")
            sys.exit(1)

        # get cursor
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "Create table if not exists UserLogin(User_Name varchar(100), Password varchar(300), Salt varchar(100), Email_ID varchar(50), Credits int, User_Games varchar(200), Primary key (User_Name))"
        )
        self.cursor.execute(
            "Create table if not exists GameScores(User_Name varchar(100), Snake integer, `2048` integer, Tetris integer, Space_wars integer, Icy integer, Foreign key (User_Name) References UserLogin(User_Name))"
        )

    def get_user_data(self):
        # check if the user exists in the database.
        check_user_query = f"SELECT * from UserLogin where User_Name = \"{self.user_data.get('user_name')}\""
        self.cursor.execute(check_user_query)
        check_user = self.cursor.rowcount
        print(check_user)
        user_data_from_maria = self.cursor.fetchone()

        print(user_data_from_maria)

        if check_user == 0:
            print("user Does not exist")
            return False
        else:
            # game scores query
            game_scores_query = f"SELECT * from GameScores where User_Name = \"{self.user_data.get('user_name')}\""
            self.cursor.execute(game_scores_query)
            game_scores_from_maria = self.cursor.fetchone()

            # Assign the game scores to the dictionary.
            self.user_game_scores['snake'] = game_scores_from_maria[1]
            self.user_game_scores['2048'] = game_scores_from_maria[2]
            self.user_game_scores['tetris'] = game_scores_from_maria[3]
            self.user_game_scores['space wars'] = game_scores_from_maria[4]
            self.user_game_scores['Icy'] = game_scores_from_maria[5]


            # assign the data to the dictionary.
            self.user_data['user_name'] = user_data_from_maria[0]
            self.user_data['user_pass_hash'] = user_data_from_maria[1]
            self.user_data['user_salt'] = user_data_from_maria[2]
            self.user_data['user_email'] = user_data_from_maria[3]
            self.user_data['user_score'] = user_data_from_maria[4]
            self.user_data['user_games'] = user_data_from_maria[5].strip('()\'').split(',')
            self.user_data['user_games'] = [x.strip().strip('\'') for x in self.user_data['user_games']]
            print(self.user_data)
            return True
    
    def insert_user(self):
        """Adds a new user to the database.
        Returns:
            Boolean : True if the new user was added successfully, False otherwise.
        """

        # salt the password
        self.user_data['user_salt'] = self.generate_random_string(10)
        print(self.user_data['user_salt'])
        self.user_data['user_pass_hash'] = self.user_data['user_pass_hash'] + self.user_data['user_salt']
        self.user_data['user_pass_hash'] = find_hash(self.user_data['user_pass_hash'])

        try:
            # Updating the User Login Table
            user_login_query = f"Insert into UserLogin values(\"{self.user_data.get('user_name')}\", \"{self.user_data.get('user_pass_hash')}\", \"{self.user_data.get('user_salt')}\", \"{self.user_data.get('user_email')}\", {self.user_data.get('user_score')} ,\"{tuple(self.user_data.get('user_games'))}\")"
            self.cursor.execute(user_login_query)

            # Updating the GameScores Table
            game_score_query = f"Insert into GameScores values(\"{self.user_data.get('user_name')}\", {self.user_game_scores.get('snake')}, {self.user_game_scores.get('2048')}, {self.user_game_scores.get('tetris')}, {self.user_game_scores.get('space wars')}, {self.user_game_scores.get('Icy')})"
            self.cursor.execute(game_score_query)

            self.connection.commit()
            print("User Added Successfully")
            return True
        except mariadb.IntegrityError as err:
            print("User Already Exists in the Table")
            return False

    def update_user_password(self):
        """updates the user data in the database. To be called only when forgot password
        Returns: True if the password was updated successfully, False otherwise. 
        """
        # salt the password
        self.user_data['user_salt'] = self.generate_random_string(10)
        print(self.user_data['user_salt'])
        self.user_data['user_pass_hash'] = self.user_data['user_pass_hash'] + self.user_data['user_salt']
        self.user_data['user_pass_hash'] = find_hash(self.user_data['user_pass_hash'])

        try:
            query = f"update UserLogin set Password = \"{self.user_data.get('user_pass_hash')}\" , Salt = \"{self.user_data.get('user_salt')}\" where User_Name = \"{self.user_data.get('user_name')}\""
            print(query)
            self.cursor.execute(query)
            self.connection.commit()
            print("User Password Updated Successfully")
            return True
        except Exception as err:
            print("error occured while updating the user data", err)
            return False

    def update_database(self):
        """
        updates the database with the new user data.
        """
        try:
            # update the user login table
            user_login_query = f"update UserLogin set Password = \"{self.user_data.get('user_pass_hash')}\" , Salt = \"{self.user_data.get('user_salt')}\", Credits = {self.user_data.get('user_score')}, User_Games = \"{tuple(self.user_data.get('user_games'))}\" where User_Name = \"{self.user_data.get('user_name')}\" "

            self.cursor.execute(user_login_query)

            # update the game scores table
            game_scores_query = f"update GameScores set Snake = {self.user_game_scores.get('snake')}, `2048` = {self.user_game_scores.get('2048')}, Tetris = {self.user_game_scores.get('tetris')}, Space_wars = {self.user_game_scores.get('space wars')}, Icy = {self.user_game_scores.get('Icy')} where User_Name = \"{self.user_data.get('user_name')}\""

            self.cursor.execute(game_scores_query)

            self.connection.commit()
            print("User Data Updated Successfully")
        except Exception as err:
            print("error occured while updating the user data", err)
        pass

    def get_top_scores(self):
        """
        stores the data of the top 10 scores in the self.top_scores dictionary.
        """
        score_query = "select *, Snake + `2048` + Tetris + Space_wars + Icy as Total from GameScores order by Snake + `2048` + Tetris + Space_wars + Icy desc limit 10"
        self.cursor.execute(score_query)
        self.top_scores = self.cursor.fetchall()


if __name__ == "__main__":
    # db = database_manager()
    # db.connect_and_create_tables()
    # db.insert_user()
    # db.get_user_data()
    # db.update_user_password()
    # db.update_database()
    # db.get_top_scores()
    pass
