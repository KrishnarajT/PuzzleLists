    # This is the file that manages all database related tasks.
    # import mysql.connector
    import sys
    import mariadb


    class database_manager:
        """class to manage all database related tasks."""

<<<<<<< HEAD
        def __init__(self):
            # initialize some stuff
            # here this thing is not instantly called coz we wont be multithreading the creation of the object,
            # only rather its methods.
            # self.connection_obj = None
            self.user_game_scores = {
                '2048' : 0,
                'Icy' : 0,  
                'snake': 0,
                'tetris': 0,
                'space wars': 0,
            }
            self.user_data = {
                "user_name": None,
                "user_email": None,
                "user_pass_hash": None
            }
            self.total_score = self.find_total_score()
            self.top_scores = None

        def find_total_score(self):
            """
            returns the total score of the user.
            """
            self.total_score = 0
            for game in self.user_game_scores:
                self.total_score += self.user_game_scores[game]
=======
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
>>>>>>> 697ccfa2628d8e7f4d79735d4eb5696251846dbc

        def connect(self):
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
            self.cur.execute("Create table if not exists UserLogin(User_ID integer, User_Name varchar(50), Password varchar(50), Email_ID varchar(50) , Primary key (User_ID))")
            self.cur.execute("Create table if not exists GameScores(User_ID integer, Snake integer, 2048 integer, Tetris integer, Space_wars integer, Icy integer, Foreign key (User_ID) References UserLogin(User_ID))")

<<<<<<< HEAD
=======
    def get_user_data(self, user_name):
        """
        If the user is present, it returns True and the data is stored in the self.user_data dictionary.
        Else it returns False.
        """
        check_user = f"SELECT User_Name from UserLogin where User_Name= {user_name}"
        if not check_user:
            print("user Does not exist")
            return False
        else:
            # assign the data to the dictionary.
            self.user_data["user_name"] = user_name
            self.user_data["user_pass_hash"] = self.cur.execute(
                f"select Password from UserLogin where User_Name={user_name}"
            )
            self.user_data["user_email"] = self.cur.execute(
                f"select Email_ID from UserLogin where User_Name={user_name}"
            )
            return True
        # connect to mariadb somehow.
>>>>>>> 697ccfa2628d8e7f4d79735d4eb5696251846dbc


        def get_user_data(self, user_name):
            """
            If the user is present, it returns True and the data is stored in the self.user_data dictionary.
            Else it returns False.
            """
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
        

        def update_login_table(self, user_name, password_hash, user_email):
            """
            updates the database with the new user data.
            """
            # insert_new_user = f"insert IGNORE into UserLogin({user_name})"
            cursor = mariadb.Connection.cursor(mariadb.Cursor.DictCursor)
            cursor.execute("select User_Name from UserLogin where username= %s",{user_name})
            check = cursor.fetchone()

            if check:
                print ("account already Exist")
                return 0
            else:
                self.cur.execute(f"Insert into UserLogin(Null,{user_name},{password_hash},{user_email})")
                print("user registered")
            

<<<<<<< HEAD

        def update_scores(self, user_name, score, game):
            """
            updates the database with the new user data.
            """
            pass

        def get_top_scores(self):
            """
            stores the data of the top 10 scores in the self.top_scores dictionary. 
            """
            pass
=======
    def update_database(self):
        """
        updates the entire database with whatever information that we have at the moment.
        """
        pass

    def get_top_scores(self):
        """
        stores the data of the top 10 scores in the self.top_scores dictionary.
        """
        pass
>>>>>>> 697ccfa2628d8e7f4d79735d4eb5696251846dbc
