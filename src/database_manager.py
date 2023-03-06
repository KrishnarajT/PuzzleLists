# This is the file that manages all database related tasks.
# import mysql.connector
import sys
import mariadb


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
            "user_name": None,
            "user_email": None,
            "user_pass_hash": None,
            "user_score": 0,
            "user_games": [],
        }
        self.top_scores = None
        self.games_owned_by_user = ["snake", "tetris"]

    def connect_and_create_tables(self):
        """forms connection with sql, and returns True.
            or else returns False
        Returns:
            _type_: _description_
        """
        try: 
            con = mariadb.connect(
                user = "parth",
                password = "4123",
                host ="127.0.0.1",
                port = 3306,
                database="Puzzlelists"
        )
        except mariadb.Error as ex:
            print(f"An error occurred while connecting to MariaDB: {ex}")
            sys.exit(1)

        # get cursor 
        self.cur = con.cursor()
        self.cur.execute("Create table if not exists UserLogin(User_ID integer, User_Name varchar(50), Password varchar(50), Email_ID varchar(50), Credits int, User_Games varchar(200) Primary key (User_ID))")
        self.cur.execute("Create table if not exists GameScores(User_ID integer, Snake integer, 2048 integer, Tetris integer, Space_wars integer, Icy integer, Foreign key (User_ID) References UserLogin(User_ID))")

    def get_user_data(self, user_name):
        check_user = f"SELECT User_Name from UserLogin where User_Name= {user_name}"
        if not check_user:
            print("user Does not exist")
            return False
        else:
            # assign the data to the dictionary.
            self.user_data['user_name'] = user_name
            self.user_data['user_pass_hash'] = self.cur.execute(
                f"select Password from UserLogin where User_Name={user_name}"
            )
            self.user_data['user_email'] = self.cur.execute(
                f"select Email_ID from UserLogin where User_Name={user_name}"
            )
            return True

    def add_user(self):
        # insert_new_user = f"insert IGNORE into UserLogin({user_name})"
        cursor = mariadb.Connection.cursor(mariadb.Cursor.DictCursor)
        cursor.execute(f"select User_Name from UserLogin where username = {self.user_data.get('user_name')}")
        check = cursor.fetchone()

        if check:
            print ("account already Exist")
            return 0
        else:
            self.cur.execute(f"Insert into UserLogin(Null,{self.user_data.get('user_name')},{self.user_data.get('user_pass_hash')},{self.user_data.get('user_email')})")
            print("user registered")

    def update_database(self):
        """
        updates the database with the new user data.
        """
        

    def get_top_scores(self):
        """
        stores the data of the top 10 scores in the self.top_scores dictionary.
        """
        pass
