
import os
import hashlib
import hmac


class AuthenticationError(Exception):
    """Raised when authentication fails."""


class MasterAuthentication:

    SALT_LENGTH = 16
    HASH_LENGTH = 32

    SCRYPT_N = 2**14
    SCRYPT_R = 8
    SCRYPT_P = 1

    MIN_PASSWORD_LENGTH = 10

    @staticmethod
    def _validate_password(password: str):

        if not isinstance(password, str):
            raise AuthenticationError(
                "Password must be text."
            )

        if len(password) < MasterAuthentication.MIN_PASSWORD_LENGTH:
            raise AuthenticationError(
                "Master password must contain at least 10 characters."
            )

    @staticmethod
    def _derive_hash(password: str, salt: bytes) -> bytes:

        return hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=MasterAuthentication.SCRYPT_N,
            r=MasterAuthentication.SCRYPT_R,
            p=MasterAuthentication.SCRYPT_P,
            dklen=MasterAuthentication.HASH_LENGTH,
        )

    @staticmethod
    def create_master_record(password: str) -> dict:
        """
        Create a record to store during master account setup.
        Never stores the original password.
        """

        MasterAuthentication._validate_password(password)

        salt = os.urandom(
            MasterAuthentication.SALT_LENGTH
        )

        password_hash = MasterAuthentication._derive_hash(
            password,
            salt,
        )

        return {
            "algorithm": "scrypt",
            "salt": salt.hex(),
            "password_hash": password_hash.hex(),
            "version": 1,
        }

    @staticmethod
    def verify_master_password(
        password: str,
        stored_record: dict,
    ) -> bool:
        """
        Verify a master password against its stored record.
        """

        try:
            if not isinstance(password, str):
                return False

            if stored_record.get("algorithm") != "scrypt":
                return False

            if stored_record.get("version") != 1:
                return False

            salt = bytes.fromhex(stored_record["salt"])

            expected_hash = bytes.fromhex(
                stored_record["password_hash"]
            )

            if len(salt) != MasterAuthentication.SALT_LENGTH:
                return False

            if len(expected_hash) != MasterAuthentication.HASH_LENGTH:
                return False

            actual_hash = MasterAuthentication._derive_hash(
                password,
                salt,
            )

            return hmac.compare_digest(
                actual_hash,
                expected_hash,
            )

        except (ValueError, TypeError, KeyError):
            return False
        except Exception:
            return False
