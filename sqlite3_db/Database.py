__author__ = "Theodoros Siklafidis"
__name__ = "Gratis"
__version__ = "1.0"
__license__ = "GNU General Public License v3.0"

import sqlite3
from cryptography.fernet import Fernet
from os_recon.define_os import path_escape
import json


class Connection:
    def __init__(self):
        """ Init function creates a .sqlite file if it doesn't already exists and connects with it. """

        self.db = sqlite3.connect(f"Output_Files{path_escape}db.sqlite")
        self.cursor = self.db.cursor()

        # Key generated with Fernet.generate_key() --> b'_irWyTD7X1KHYq0UiBdY9yECvBFpY_MLyOD3AOrpMYM='
        self.key = b'_irWyTD7X1KHYq0UiBdY9yECvBFpY_MLyOD3AOrpMYM='  # Encryption key for fernet.
        self.cipher_suite = Fernet(self.key)                        # Fernet object with the specified key above.
        
    def encrypt(self, value_to_encrypt):
        cipher_text = self.cipher_suite.encrypt(str(value_to_encrypt).encode('utf-8'))
        return str(cipher_text, 'utf-8')

    def decrypt(self, value_to_decode):
        plain_text = self.cipher_suite.decrypt(str(value_to_decode).encode('utf-8'))
        return str(plain_text, 'utf-8')
    
    def close(self):
        self.cursor.close()
        self.db.close()
        return True


class User(Connection):
    def __init__(self):
        super().__init__()
        self.initiate_user_table()
    
    def initiate_user_table(self):
        self.db.execute("""CREATE TABLE IF NOT EXISTS `user` 
                            (
                                `id` INTEGER PRIMARY KEY AUTOINCREMENT, 
                                `username` TEXT, 
                                `api_key` TEXT
                            )
                        """)
        return True


    def create(self, username, api_key):
        encrypted_username = self.encrypt(username)
        encrypted_api_key = self.encrypt(api_key)

        if self.check_user():
            self.db.execute("DELETE FROM user")

        self.db.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'user'")
        self.db.execute("INSERT INTO 'user'('username', 'api_key') VALUES (?, ?)",
                        (encrypted_username, encrypted_api_key))
        self.db.commit()
    
    def delete(self):
        self.db.execute('DELETE FROM user')
        self.db.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'user'")
        self.db.commit()
    
    def get_credentials(self):
        results = self.db.execute('SELECT * from user limit 1')
        credentials = results.fetchone()
        try:
            decrypted_username = self.decrypt(credentials[1])
            decrypted_api_key = self.decrypt(credentials[2])

            return decrypted_username, decrypted_api_key
        except TypeError:
            pass
    
    def check_user(self):
        results = self.db.execute('SELECT * from user limit 1')
        existence = results.fetchone()
        if existence:
            return True
        else:
            return False


class Graph(Connection):
    def __init__(self):
        super().__init__()
        self.initiate_graph_history_table()
        
    def initiate_graph_history_table(self):
        self.db.execute("""CREATE TABLE IF NOT EXISTS `graph_history` 
                            (
                                `id` INTEGER PRIMARY KEY AUTOINCREMENT, 
                                `attributes` TEXT, 
                                `created_at` TEXT
                            )
                        """)
        return True

    def create(self, attributes):
        self.cursor.execute("INSERT INTO `graph_history`(`attributes`, `created_at`) VALUES(?, datetime('now','localtime'))", (json.dumps(attributes),))
        self.db.commit()
        return True

    def delete(self, graph_id):
        self.cursor.execute('DELETE FROM `graph_history` WHERE `id`=?', (graph_id,))
        self.db.commit()
        return True
    
    def all(self):
        graph_objects = self.cursor.execute("SELECT * FROM `graph_history` ORDER BY `id` DESC")
        return graph_objects

    def count(self):
        number_of_graph_objects = self.cursor.execute("SELECT COUNT(*) FROM `graph_history`").fetchone()[0]
        return(number_of_graph_objects)

    def populate(self, N):
        import random
        graph_respresentation_type = ["Matrix", "List"]
        graph_type = [
            "Homogeneous",
            "Erdos Renyi Graph", 
            "Custom Full Scale Free Graph", 
            "Full Scale Free Graph", 
            "Random Fixed Graph", 
            "Custom Scale Free Graph with Preferential Attachment", 
            "Scale Free Graph with Preferential Attachment"
            ]

        for i in range(N):
            attrs = {
                    'Graph_Respresentation_Type': random.choice(graph_respresentation_type),
                    'Graph_Type': random.choice(graph_type),
                    'Number_Of_Vertices': random.randint(2, 1000),
                    'Graph_Degree': random.randint(2, 1000),
                    'Number_Of_Maximum_Edges': random.randint(2, 1000),
                    'Number_Of_Initial_Nodes': random.randint(2, 1000),
                    'Initial_Connections_Per_Node': random.randint(2, 1000),
                    'Probability': random.randint(2, 1000),
                    'Seed': random.randint(2, 1000),
                    }

            self.create(attrs)