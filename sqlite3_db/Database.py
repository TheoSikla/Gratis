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
        
        # for graph in self.all():
        #     print(f"ID: {graph[0]}")
        #     for k, v in json.loads(graph[1]).items():
        #         print(f"{k}: {v}")
        #     print(f"Generated at: {graph[2]}")

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
        self.db.execute("INSERT INTO `graph_history`(`attributes`, `created_at`) VALUES(?, datetime('now','localtime'))", (json.dumps(attributes),))
        self.db.commit()

    def delete(self, graph_id):
        self.db.execute('DELETE FROM `graph_history` WHERE `id`=?', (graph_id))
        self.db.commit()
    
    def all(self):
        graph_objects = self.db.execute("SELECT * FROM `graph_history`")
        return graph_objects

# class Connection:

#     def __init__(self):
#         """ Init function creates a .sqlite file if it doesn't already exists and connects with it. """

#         self.db = sqlite3.connect(f"Output_Files{path_escape}latest_credentials.sqlite")
#         self.db.execute("CREATE TABLE IF NOT EXISTS `last_user`(`id` INTEGER PRIMARY KEY AUTOINCREMENT,"
#                         " `username` TEXT, `api_key`	TEXT)")
#         self.cursor = self.db.cursor()

#         # Key generated with Fernet.generate_key() --> b'_irWyTD7X1KHYq0UiBdY9yECvBFpY_MLyOD3AOrpMYM='
#         self.key = b'_irWyTD7X1KHYq0UiBdY9yECvBFpY_MLyOD3AOrpMYM='  # Encryption key for fernet.
#         self.cipher_suite = Fernet(self.key)                        # Fernet object with the specified key above.

#     def Insert(self, username, api_key):
#         flag = self.Db_check()
#         encrypted_username = self.encrypt(username)
#         encrypted_api_key = self.encrypt(api_key)

#         if flag is False:
#             self.db.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'last_user'")
#             self.db.execute("INSERT INTO 'last_user'('username', 'api_key') VALUES (?, ?)",
#                             (encrypted_username, encrypted_api_key))
#             self.db.commit()
#         else:
#             self.db.execute("DELETE FROM last_user")
#             self.db.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'last_user'")
#             self.db.execute("INSERT INTO 'last_user'('username', 'api_key') VALUES (?, ?)",
#                             (encrypted_username, encrypted_api_key))
#             self.db.commit()

#     def Delete(self):
#         self.db.execute('DELETE FROM last_user')
#         self.db.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'last_user'")
#         self.db.commit()

#     def Db_check(self):
#         results = self.db.execute('SELECT * from last_user limit 1')
#         existence = results.fetchone()
#         if existence:
#             return True
#         else:
#             return False

#     def Get_creds(self):
#         results = self.db.execute('SELECT * from last_user limit 1')
#         credentials = results.fetchone()
#         try:
#             decrypted_username = self.decrypt(credentials[1])
#             decrypted_api_key = self.decrypt(credentials[2])

#             return decrypted_username, decrypted_api_key
#         except TypeError:
#             pass

#     def encrypt(self, value_to_encrypt):
#         cipher_text = self.cipher_suite.encrypt(str(value_to_encrypt).encode('utf-8'))
#         return str(cipher_text, 'utf-8')

#     def decrypt(self, value_to_decode):
#         plain_text = self.cipher_suite.decrypt(str(value_to_decode).encode('utf-8'))
#         return str(plain_text, 'utf-8')

#     def Close(self):
#         self.cursor.close()
#         self.db.close()
