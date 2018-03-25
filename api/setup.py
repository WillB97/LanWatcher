from pymongo import MongoClient
import pymongo
import json
import hashlib
from os import urandom

adminPwd = input("Enter admin password:")
user = input("Enter username:")
pwd = input("Enter user password:")

client = MongoClient()
# client = MongoClient(username='user', password='pwd', authSource='admin')
db = client.LanScan # create database
client.admin.command("createUser", "admin", pwd=adminPwd,
		roles=[{"role": "readWriteAnyDatabase", "db": "admin"},
			{"role": "userAdminAnyDatabase", "db": "admin"}]) # create admin user

db.command("createUser", user, pwd=pwd,
		roles=[{"role": "readWrite", "db": "LanScan"}]) # create worker user and config
with open('config.json','w') as fs:
	json.dump({"user": user, "pwd": pwd, "secret": urandom(64).hex()}, fs, indent="\t")

db.create_collection('users') # create users and keys collections
db.users.create_index([('user', pymongo.DESCENDING)], unique=True)
db.create_collection('keys')
db.users.create_index([('keyphrase', pymongo.DESCENDING)], unique=True)
salt = urandom(16).hex().upper()
pass_hash = hashlib.sha256(str('admin' + salt).encode('utf-8')).hexdigest()
db['users'].insert_one({'user':'admin','pass':pass_hash,'salt':salt}) # add default user to collection