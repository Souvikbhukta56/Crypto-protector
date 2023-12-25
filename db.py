import mysql.connector
from passlib.hash import bcrypt

config = {
    'database': 'crypto_protector',
    'user': 'Scorpion7',
    'password': 'Souvik@7',
    'host': 'Oxen7', 
    'port': '3306',      
    'raise_on_warnings': True,
}

class DB:
    def create_user_table():
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        user_table = """
            CREATE TABLE IF NOT EXISTS User (
                uname VARCHAR(255) primary key,
                email VARCHAR(255) not null,
                password VARCHAR(255) not null,
                unique(uname),
                unique(email)
            )"""
        cursor.execute(user_table)
        cursor.close()
        connection.commit()
        connection.close()

    def create_file_table():
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        file_table = """
            create table if not EXISTS File (
                file_id varchar(255),
                receiver varchar(255) not null,
                sender varchar(255) not null,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                file_name VARCHAR(255) not null,
                Foreign key (receiver) references User(uname),
                Foreign key (sender) references User(uname),
                primary key (file_id)
            )
        """
        cursor.execute(file_table)
        cursor.close()
        connection.commit()
        connection.close()
        
    def save_user_data(uname, email, password):
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = "INSERT INTO User(uname, email, password) VALUES(%s, %s, %s)"
        data = (uname, email, password)
        cursor.execute(query, data)
        connection.commit()
        connection.close()
    
    def authenticate(username, entered_password):
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = "select password from User where uname = %s"
        cursor.execute(query, (username,))
        stored_password = cursor.fetchone()
        connection.close()
        return stored_password and bcrypt.verify(entered_password, stored_password[0]) # Returns True or False

    def get_usernames():
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = "select uname from user"
        cursor.execute(query)
        usernames = cursor.fetchall()
        connection.close()
        return usernames

    def save_file(bin_id, sender, receiver, filename):
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = "INSERT INTO File(file_id, receiver, sender, file_name) VALUES(%s, %s, %s, %s)"
        data = (bin_id, receiver, sender, filename) # The bin id will be file id
        cursor.execute(query, data)
        connection.commit()
        connection.close()

    def show_files(current_user):
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = """
            select file_id, uname, upload_date, file_name 
            from File inner join User
            on sender=uname
            where file.receiver=%s
        """
        cursor.execute(query, (current_user,))
        file_details = cursor.fetchall()
        connection.close()
        return file_details
        
    def get_file_name(file_id):
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = "select file_name from File where file_id = %s"
        cursor.execute(query, (file_id,))
        result = cursor.fetchone()
        connection.close()
        return result[0]




