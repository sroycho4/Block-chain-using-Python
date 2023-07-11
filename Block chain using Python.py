import time
import hashlib as hasher
import datetime as date
from cryptography.fernet import Fernet
import pymongo

client = pymongo.MongoClient("Link to the server")
db = client.testuser750
mydb = client["newDB"]
mycol = mydb["Blockhead"]

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hasher.sha256()
        sha.update(
            str(self.index).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8')
        )
        return sha.hexdigest()

def int_list_to_hex(l):
    return ''.join("{0:0{1}x}".format(x, 2) for x in l)

def int_list_to_string(l):
    return ''.join(chr(x) for x in l)

mylist = mycol.find_one()
blockchain = [Block(0, date.datetime.now(), mylist, "0")]

# Encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)
encrypted_data = cipher_suite.encrypt(str(mylist).encode())
print('encrypted ciphertext:'.ljust(24), encrypted_data.decode())

# Decryption
decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
print('decrypted plaintext:'.ljust(24), decrypted_data)

# Compare the encrypted and decrypted data for validity
if str(mylist) == decrypted_data:
    print('Data is valid')
else:
    print('Data is not valid')

def validate_blockchain(blockchain):
    for i in range(1, len(blockchain)):
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]

        if current_block.hash != current_block.calculate_hash():
            return False
        
        if current_block.previous_hash != previous_block.hash:
            return False

    return True

is_valid = validate_blockchain(blockchain)
if is_valid:
    print("Blockchain is valid!")
else:
    print("Blockchain is not valid!")

# Perform time-based encryption and decryption
start_time = time.time()
# Encryption
encrypted_data = cipher_suite.encrypt(str(mylist).encode())
print('encrypted ciphertext:'.ljust(24), encrypted_data.decode())
time.sleep(120)  # Wait for 2 minutes
end_time = time.time()
if end_time - start_time >= 120:
    # Decryption
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    print('decrypted plaintext:'.ljust(24), decrypted_data)
    if str(mylist) == decrypted_data:
        print('Data is valid')
    else:
        print('Data is not valid')
else:
    print('Time period not elapsed')

# Validate the blockchain
is_valid = validate_blockchain(blockchain)
if is_valid:
    print("Blockchain is valid!")
else:
    print("Blockchain is not valid!")

