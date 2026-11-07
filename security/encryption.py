
import os
import json
import base64
import hashlib

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class EncryptionError(Exception):
    """Raised when encryption or decryption fails."""


class PasswordEncryption:

    VERSION = 1
    KEY_LENGTH = 32
    SALT_LENGTH = 16
    NONCE_LENGTH = 12

    # Scrypt key derivation parameters
    SCRYPT_N = 2**14
    SCRYPT_R = 8
    SCRYPT_P = 1

    @staticmethod
    def _derive_key(master_password: str, salt: bytes) -> bytes:

        if not isinstance(master_password, str) or not master_password:
            raise ValueError("Master password cannot be empty.")

        return hashlib.scrypt(
            master_password.encode("utf-8"),
            salt=salt,
            n=PasswordEncryption.SCRYPT_N,
            r=PasswordEncryption.SCRYPT_R,
            p=PasswordEncryption.SCRYPT_P,
            dklen=PasswordEncryption.KEY_LENGTH,
        )

    @staticmethod
    def encrypt(plaintext: str, master_password: str) -> str:
        """
        Encrypt a password or other text.
        Returns a versioned Base64-encoded JSON envelope.
        """

        if not isinstance(plaintext, str):
            raise TypeError("Plaintext must be a string.")

        try:
            salt = os.urandom(PasswordEncryption.SALT_LENGTH)
            nonce = os.urandom(PasswordEncryption.NONCE_LENGTH)

            key = PasswordEncryption._derive_key(
                master_password,
                salt,
            )

            aes = AESGCM(key)

            ciphertext = aes.encrypt(
                nonce,
                plaintext.encode("utf-8"),
                b"CloudPass-v1",
            )

            envelope = {
                "version": PasswordEncryption.VERSION,
                "salt": base64.b64encode(salt).decode("ascii"),
                "nonce": base64.b64encode(nonce).decode("ascii"),
                "ciphertext": base64.b64encode(
                    ciphertext
                ).decode("ascii"),
            }

            return json.dumps(envelope)

        except (ValueError, TypeError):
            raise
        except Exception as error:
            raise EncryptionError(
                "Unable to encrypt the data."
            ) from error

    @staticmethod
    def decrypt(encrypted_data: str, master_password: str) -> str:
        """
        Decrypt a CloudPass encrypted envelope.
        Raises EncryptionError if the password or data is incorrect.
        """

        try:
            envelope = json.loads(encrypted_data)

            if envelope.get("version") != PasswordEncryption.VERSION:
                raise EncryptionError(
                    "Unsupported encryption version."
                )

            salt = base64.b64decode(
                envelope["salt"],
                validate=True,
            )

            nonce = base64.b64decode(
                envelope["nonce"],
                validate=True,
            )

            ciphertext = base64.b64decode(
                envelope["ciphertext"],
                validate=True,
            )

            if len(salt) != PasswordEncryption.SALT_LENGTH:
                raise EncryptionError("Invalid salt.")

            if len(nonce) != PasswordEncryption.NONCE_LENGTH:
                raise EncryptionError("Invalid nonce.")

            key = PasswordEncryption._derive_key(
                master_password,
                salt,
            )

            aes = AESGCM(key)

            plaintext = aes.decrypt(
                nonce,
                ciphertext,
                b"CloudPass-v1",
            )

            return plaintext.decode("utf-8")

        except EncryptionError:
            raise
        except Exception as error:
            raise EncryptionError(
                "Decryption failed. Check your master password "
                "or encrypted data."
            ) from error
