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
        pass

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
        # connected = True
        # if connected:
        #     # defining the object here.
        #     self.connection_obj = None
        #     return True
        # else:
        #     return False

    def get_user_data(self, user_name):
        """
        returns the a dictionary containing information abotu the user if the user name is found.
        if the password is not found, it returns 0, meaning the username doesnt exist.
        """
        check_user = f"SELECT User_Name from UserLogin where User_Name= {user_name}"
        if not check_user:
            print("user Does not exist")
            return False
        
        else:
            usr = user_name
            pas = self.cur.execute(f"select Password from UserLogin where User_Name={user_name}")
            mail = self.cur.execute(f"select Email_ID from UserLogin where User_Name={user_name}")
            data = {
                "password_hash": pas,
                "user_name": usr,
                "user_email": mail,
            }
            return data 
        # connect to mariadb somehow.
        


        # check if the user exists using self.connection_obj or something.
        # if the user exists, return the data you got.
        # if user_exists:

        #     return data
        # else:
        #     print("User does not exist")
        #     return 0

    def update_login_table(self, user_name, password_hash, user_email):
        """
        updates the database with the new user data.
        """
        
        pass

    def update_scores(self, user_name, score, game):
        """
        updates the database with the new user data.
        """
        pass
