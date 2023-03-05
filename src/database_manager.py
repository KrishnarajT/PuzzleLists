# This is the file that manages all database related tasks.


class database_manager:
    """class to manage all database related tasks."""

    def __init__(self):
        # initialize some stuff
        # here this thing is not instantly called coz we wont be multithreading the creation of the object,
        # only rather its methods.
        self.connection_obj = None
        pass

    def connect(self):
        """forms connection with sql, and returns True.
            or else returns False
        Returns:
            _type_: _description_
        """
        connected = True
        if connected:
            # defining the object here.
            self.connection_obj = None
            return True
        else:
            return False

    def get_user_data(self, user_name):
        """
        returns the a dictionary containing information abotu the user if the user name is found.
        if the password is not found, it returns 0, meaning the username doesnt exist.
        """

        # connect to mariadb somehow.
        user_exists = True

        # check if the user exists using self.connection_obj or something.
        # if the user exists, return the data you got.
        if user_exists:
            data = {
                "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                "user_name": "username",
                "user_email": "kpt.krishnaraj@gmail.com",
            }

            return data
        else:
            print("User does not exist")
            return 0

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
