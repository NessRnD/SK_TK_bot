import sqlite3

class database:
    def __init__(self,db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self,user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id, ))

    def set_tgtag(self,user_id,tag):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `tg_name` = ? WHERE `user_id` = ?",(tag,user_id,))

    def user_exists(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id, )).fetchall()
            return bool(len(result))

    def set_name(self,user_id,name):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `name` = ? WHERE `user_id` = ?",(name,user_id,))

    def get_signup(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` = ? ",(user_id, )).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id,))

    def get_name(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `name` FROM `users` WHERE `user_id` = ? ",(user_id, )).fetchall()
            for row in result:
                name = str(row[0])
            return name

    def delete_user(self,user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `users` WHERE `user_id` = ?",(user_id, )).fetchall()
