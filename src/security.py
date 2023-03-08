# File to perform password check and security
import hashlib


def find_hash(password):
    """Find hash of password"""
    return hashlib.sha256(password.encode()).hexdigest()


if __name__ == "__main__":
    print(find_hash("Krishnaraj"))
