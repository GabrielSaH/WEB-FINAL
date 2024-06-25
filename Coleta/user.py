import bcrypt


def get_hash_and_salt(password):
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password, salt

def check_unhash(password, hashed_password , salt):
    input_hash_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8'))

    return input_hash_password == hashed_password.encode('utf-8')