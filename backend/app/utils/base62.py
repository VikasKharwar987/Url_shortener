import secrets
BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def generate_short_code(length=8):
    short_code = ""
    for _ in range(length):
        random_index = secrets.randbelow(62)
        short_code += BASE62[random_index]
    return short_code