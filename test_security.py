
from security.encryption import PasswordEncryption
from security.authentication import MasterAuthentication


# Test master authentication
master_password = "MyStrongMasterPassword123!"

record = MasterAuthentication.create_master_record(
    master_password
)

print(
    "Correct password:",
    MasterAuthentication.verify_master_password(
        master_password,
        record,
    ),
)

print(
    "Wrong password:",
    MasterAuthentication.verify_master_password(
        "WrongPassword123!",
        record,
    ),
)


# Test encryption and decryption
original_password = "ExampleWebsite@123"

encrypted = PasswordEncryption.encrypt(
    original_password,
    master_password,
)

print("\nEncrypted data:")
print(encrypted)

decrypted = PasswordEncryption.decrypt(
    encrypted,
    master_password,
)

print("\nDecrypted data:")
print(decrypted)

print("\nEncryption test:", decrypted == original_password)
