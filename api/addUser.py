from os import urandom
import hashlib
from pymongo import MongoClient
import json

user = input("Enter username:")
password = input("Enter password:")

salt = urandom(16).hex().upper()
pass_hash = hashlib.sha256(
            str(password + salt).encode('utf-8')).hexdigest()

try:
    with open('config.json') as fs:
        config = json.load(fs)
except:
    raise

client = MongoClient(username=config.get('user'), password=config.get('pwd'), authSource='LanScan')
db = client['LanScan']

db.users.insert_one({'user':user,'pass':pass_hash,'salt':salt})
