
import json
import sqlite3
from pathlib import Path

from security.encryption import PasswordEncryption
from security.authentication import MasterAuthentication


class SecureStorage:

    def __init__(self, database_path=None):

        if database_path is None:
            database_path = (
                Path(__file__).resolve().parent / "cloudpass.db"
            )

        self.database_path = str(database_path)

        Path(self.database_path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.initialize_database()

    def connect(self):
        return sqlite3.connect(self.database_path)

    def initialize_database(self):

        with self.connect() as connection:

            connection.execute("""
                CREATE TABLE IF NOT EXISTS app_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS vault_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    encrypted_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    # MASTER PASSWORD

    def has_master_password(self):

        with self.connect() as connection:

            result = connection.execute(
                """
                SELECT value
                FROM app_metadata
                WHERE key = ?
                """,
                ("master_record",),
            ).fetchone()

        return result is not None

    def create_master_password(self, password):

        if self.has_master_password():
            raise ValueError(
                "A master password has already been created."
            )

        record = MasterAuthentication.create_master_record(
            password
        )

        with self.connect() as connection:

            connection.execute(
                """
                INSERT INTO app_metadata (key, value)
                VALUES (?, ?)
                """,
                ("master_record", json.dumps(record)),
            )

    def verify_master_password(self, password):

        with self.connect() as connection:

            result = connection.execute(
                """
                SELECT value
                FROM app_metadata
                WHERE key = ?
                """,
                ("master_record",),
            ).fetchone()

        if result is None:
            return False

        try:
            record = json.loads(result[0])

            return MasterAuthentication.verify_master_password(
                password,
                record,
            )

        except (ValueError, TypeError, json.JSONDecodeError):
            return False

    # SAVE ENCRYPTED PASSWORD

    def save_password(self, password_data, master_password):

        if not self.verify_master_password(master_password):
            raise ValueError("Master password verification failed.")

        data = dict(password_data)
        data.pop("id", None)

        plaintext = json.dumps(
            data,
            ensure_ascii=False,
        )

        encrypted_data = PasswordEncryption.encrypt(
            plaintext,
            master_password,
        )

        with self.connect() as connection:

            cursor = connection.execute(
                """
                INSERT INTO vault_entries (encrypted_data)
                VALUES (?)
                """,
                (encrypted_data,),
            )

            return cursor.lastrowid

    # UPDATE ENCRYPTED PASSWORD

    def update_password(
        self,
        record_id,
        password_data,
        master_password,
    ):

        if not self.verify_master_password(master_password):
            raise ValueError("Master password verification failed.")

        data = dict(password_data)
        data.pop("id", None)

        plaintext = json.dumps(
            data,
            ensure_ascii=False,
        )

        # Encrypt the complete updated record.
        encrypted_data = PasswordEncryption.encrypt(
            plaintext,
            master_password,
        )

        with self.connect() as connection:

            cursor = connection.execute(
                """
                UPDATE vault_entries
                SET encrypted_data = ?
                WHERE id = ?
                """,
                (encrypted_data, record_id),
            )

            if cursor.rowcount == 0:
                raise ValueError("Account not found.")

    # LOAD AND DECRYPT PASSWORDS

    def get_passwords(self, master_password):

        if not self.verify_master_password(master_password):
            raise ValueError("Master password verification failed.")

        with self.connect() as connection:

            rows = connection.execute(
                """
                SELECT id, encrypted_data
                FROM vault_entries
                ORDER BY id DESC
                """
            ).fetchall()

        passwords = []

        for record_id, encrypted_data in rows:

            plaintext = PasswordEncryption.decrypt(
                encrypted_data,
                master_password,
            )

            account = json.loads(plaintext)

            if not isinstance(account, dict):
                raise ValueError("Invalid account record.")

            account["id"] = record_id

            passwords.append(account)

        return passwords

    # DELETE PASSWORD

    def delete_password(self, record_id, master_password):

        if not self.verify_master_password(master_password):
            raise ValueError("Master password verification failed.")

        with self.connect() as connection:

            cursor = connection.execute(
                """
                DELETE FROM vault_entries
                WHERE id = ?
                """,
                (record_id,),
            )

            if cursor.rowcount == 0:
                raise ValueError("Account not found.")
