import sqlite3
from cryptography.fernet import Fernet
from os_recon.define_os import path_escape


class Connection:

    # Init function creates a .sqlite file if it doesn't already exists and connects with it.
    def __init__(self):
        self.db = sqlite3.connect("Output_Files{}latest_credentials.sqlite".format(path_escape))
        self.db.execute("CREATE TABLE IF NOT EXISTS `last_user`(`id` INTEGER PRIMARY KEY AUTOINCREMENT,"
                        " `username` TEXT, `api_key`	TEXT)")
        self.cursor = self.db.cursor()

        # Key generated with Fernet.generate_key() --> b'_irWyTD7X1KHYq0UiBdY9yECvBFpY_MLyOD3AOrpMYM='
        self.key = b'_irWyTD7X1KHYq0UiBdY9yECvBFpY_MLyOD3AOrpMYM='  # Encryption key for fernet.
        self.cipher_suite = Fernet(self.key)  # Fernet object with the specified key above.
    # ==================================================================================================================

    # Insert function registers one user in the database.
    def Insert(self, username, api_key):
        flag = self.Db_check()
        encrypted_username = self.encrypt(username)
        encrypted_api_key = self.encrypt(api_key)

        if flag is False:

            self.db.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'last_user'")
            self.db.execute("INSERT INTO 'last_user'('username', 'api_key') VALUES (?, ?)",
                            (encrypted_username, encrypted_api_key))
            self.db.commit()
        else:
            self.db.execute("DELETE FROM last_user")

            self.db.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'last_user'")

            self.db.execute("INSERT INTO 'last_user'('username', 'api_key') VALUES (?, ?)",
                            (encrypted_username, encrypted_api_key))
            self.db.commit()
    # ==================================================================================================================

    # Delete function deletes a user if he does exist in the database.
    def Delete(self):
        self.db.execute('DELETE FROM last_user')
        self.db.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'last_user'")
        self.db.commit()
    # ==================================================================================================================

    # Db_check function checks if there is a user in the database or not.
    def Db_check(self):
        results = self.db.execute('SELECT * from last_user limit 1')
        existence = results.fetchone()
        if existence:
            return True
        else:
            return False
    # ==================================================================================================================

    # Get_creds function retrieves user credentials.
    def Get_creds(self):
        results = self.db.execute('SELECT * from last_user limit 1')
        credentials = results.fetchone()
        try:
            decrypted_username = self.decrypt(credentials[1])
            decrypted_api_key = self.decrypt(credentials[2])

            return decrypted_username, decrypted_api_key
        except TypeError:
            pass
    # ==================================================================================================================

    # Fernet Encrypt
    def encrypt(self, value_to_encrypt):
        cipher_text = self.cipher_suite.encrypt(str(value_to_encrypt).encode('utf-8'))
        return str(cipher_text, 'utf-8')
    # ==================================================================================================================

    # Fernet Decrypt
    def decrypt(self, value_to_decode):
        plain_text = self.cipher_suite.decrypt(str(value_to_decode).encode('utf-8'))
        return str(plain_text, 'utf-8')
    # ==================================================================================================================

    # Close function closes the cursor and terminates the connection.
    def Close(self):
        self.cursor.close()
        self.db.close()
    # ==================================================================================================================
