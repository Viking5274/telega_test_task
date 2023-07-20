import sqlite3


class MyDb:
    def __init__(self, name):
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()
        self.create_if_not_exist()

    def create_if_not_exist(self):
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS posts(
                [user_id] INTEGER, 
                [post_text] TEXT, 
                [media_data] TEXT,
                [post_author] TEXT, 
                [date_created] TEXT, 
                [link] TEXT) 
            """
        )

        self.conn.commit()

    def check_if_exist(self, link):
        print(link)
        self.cursor.execute("SELECT link FROM posts WHERE link = ?", (link,))
        exists = self.cursor.fetchall()
        if exists:
            print('This post already exist in db')
            return True

        return False

    def save_to_db(self, data):

        if not self.check_if_exist(data[5]):
            self.cursor.execute("INSERT INTO posts VALUES(?, ?, ?, ?, ?, ?)", data)
            self.conn.commit()
            print('saved successfully')