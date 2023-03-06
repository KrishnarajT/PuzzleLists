# This is the file that manages all database related tasks.
# import mysql.connector
import sys
import mariadb
from security import find_hash

class database_manager:
    """class to manage all database related tasks."""

    def __init__(self):
        # initialize some stuff
        # here this thing is not instantly called coz we wont be multithreading the creation of the object,
        # only rather its methods.
        # self.connection_obj = None
        self.user_game_scores = {
            "2048": 0,
            "Icy": 0,
            "snake": 0,
            "tetris": 0,
            "space wars": 0,
        }
        self.user_data = {
            "user_name": 'abcd',
            "user_email": 'abde@adfa',
            "user_pass_hash": find_hash("password"),
            "user_score": 0,
            "user_games": ["snake", "tetris"],
        }
        self.top_scores = None
        self.cursor = None
        self.games_owned_by_user = ["snake", "tetris"]

    def connect_and_create_tables(self):
        """forms connection with sql, and returns True.
            or else returns False
        Returns:
            _type_: _description_
        """
        try: 
            con = mariadb.connect(
                user = "krishnaraj",
                password = "mariamaria",
                host ="127.0.0.1",
                port = 3306,
                database="Puzzlelists"
        )
        except mariadb.Error as ex:
            print(f"An error occurred while connecting to MariaDB: {ex}")
            sys.exit(1)

        # get cursor 
        self.cursor = con.cursor()
        self.cursor.execute("Create table if not exists UserLogin(User_Name varchar(100), Password varchar(300), Email_ID varchar(50), Credits int, User_Games varchar(200), Primary key (User_Name))")
        self.cursor.execute("Create table if not exists GameScores(User_Name varchar(100), Snake integer, `2048` integer, Tetris integer, Space_wars integer, Icy integer, Foreign key (User_Name) References UserLogin(User_Name))")

    def get_user_data(self, user_name):
        check_user = f"SELECT User_Name from UserLogin where User_Name= {user_name}"
        if not check_user:
            print("user Does not exist")
            return False
        else:
            # assign the data to the dictionary.
            self.user_data['user_name'] = user_name
            self.user_data['user_pass_hash'] = self.cursor.execute(
                f"select Password from UserLogin where User_Name={user_name}"
            )
            self.user_data['user_email'] = self.cursor.execute(
                f"select Email_ID from UserLogin where User_Name={user_name}"
            )
            return True

    def add_user(self):
        """Adds a new user to the database.
        Returns:
            Boolean : True if the new user was added successfully, False otherwise.
        """        

        check = self.cursor.execute(f"Insert into UserLogin values(\"{self.user_data.get('user_name')}\", \"{self.user_data.get('user_pass_hash')}\", \"{self.user_data.get('user_email')}\", {self.user_data.get('user_score')} ,\"{tuple(self.user_data.get('user_games'))}\")")
        print(check)

        if check:
            print ("account already Exist")
            return False
        else:
            print("user registered")
            return True

    def update_user(self):
        """updates the user data in the database.
        """
        pass
    def update_database(self):
        """
        updates the database with the new user data.
        """
        

    def get_top_scores(self):
        """
        stores the data of the top 10 scores in the self.top_scores dictionary.
        """
        pass


if __name__ == "__main__":
    db = database_manager()
    db.connect_and_create_tables()
    db.add_user()