import jwt
from datetime import datetime, timedelta
import hashlib
from flask import request
from flask_restful import reqparse, Resource, inputs
import os


class login_endpoint(Resource):
    """Generate user-level authentication tokens from provided credentials"""

    def __init__(self, db, secret, auth):
        self.users = db.users
        self.auth_secret = secret
        self.auth_test = auth.auth_test

    def post(self):
        # Validate user input
        postParse = reqparse.RequestParser()
        postParse.add_argument('username', required=True, location='form',
                               nullable=False, type=inputs.regex(r'^[A-Za-z0-9 ]{1,32}$'))
        postParse.add_argument('password', required=True, location='form', nullable=False)
        args = postParse.parse_args()
        # Fetch record from database
        record = self.users.find_one({'user': args['username']})  # retrieve record from database
        if record is None:
            return {'token': None}, 403
        # Test for password match
        pass_hash = hashlib.sha256(
            str(args['password'] + record['salt']).encode('utf-8')).hexdigest()
        if record['pass'] == pass_hash:
            # Generate token
            token = jwt.encode({'user': args['username'],
                'exp': datetime.utcnow() + timedelta(hours=2), # Expiry after 2 hours
                'nbf': datetime.utcnow(), # Not usable before now
                'iat': datetime.utcnow()}, # Issued at
                self.auth_secret, algorithm='HS256').decode("utf-8")
            return {'token': token}
        else:
            return {'token': None}, 403

    def put(self):
        putParse = reqparse.RequestParser()
        putParse.add_argument('password', required=True, location='form', nullable=False)
        auth = self.auth_test({}, request.cookies, '') # test auth
        args = putParse.parse_args()
        if auth != True:
            return auth
        user = jwt.decode(request.cookies['token'], self.auth_secret, algorithm='HS256').get('user')
        record = self.users.find_one({'user': user})
        pass_hash = hashlib.sha256(
            str(args['password'] + record.get('salt')).encode('utf-8')).hexdigest()
        result = self.users.update_one({'user': user},{'$set': {'pass': pass_hash}}) # update record
        if result.modified_count != 1:
            return {'success': False}, 500
        return {'success': True}, 201


class keys_endpoint(Resource):
    """Manage API keys associated with the authenticated user"""

    def __init__(self, db, secret, auth):
        self.keys = db.keys
        self.auth_secret = secret
        self.auth_test = auth.auth_test

    def get(self):
        auth = self.auth_test({}, request.cookies, '') # test auth
        if auth != True:
            return auth
        user = jwt.decode(request.cookies['token'], self.auth_secret, algorithm='HS256').get('user')
        result = self.keys.find({'user': user}, {'_id': 0, 'user': 0}) # get key records for user
        return {'data': list(result)}

    def post(self):
        postParse = reqparse.RequestParser()
        postParse.add_argument('vlan', required=True, location='form', action='append',
                                nullable=False, type=inputs.regex(r'^[A-Za-z0-9]{1,32}$'))
        postParse.add_argument('expiry', required=False, location='form', type=float)
        auth = self.auth_test({}, request.cookies, '') # test auth
        args = postParse.parse_args()
        if auth != True:
            return auth
        user = jwt.decode(request.cookies['token'], self.auth_secret, algorithm='HS256').get('user')
        keyphrase = os.urandom(8).hex().upper() # generate new key
        # TODO: check key is unique
        key = {"keyphrase": keyphrase, "user": user, "vlan": args['vlan'], "expiry": 0}
        token_data = {'key': keyphrase,
                'nbf': datetime.utcnow(), # Not usable before now
                'iat': datetime.utcnow()} # Issued at
        if args['expiry'] != None and args['expiry'] >= 0:
            key["expiry"] = (datetime.utcnow() + timedelta(hours=args['expiry'])).timestamp()
            token_data['exp'] = datetime.utcnow() + timedelta(hours=args['expiry']) # Add expiry to token
        self.keys.insert_one(key) # insert key into database
        token = jwt.encode(token_data, self.auth_secret, algorithm='HS256').decode("utf-8") # return key and ID
        return {'auth-token': token, 'keyphrase': keyphrase}, 201

    def put(self):
        putParse = reqparse.RequestParser()
        putParse.add_argument('keyphrase', required=True, location='form',
                                nullable=False, type=inputs.regex(r'^[A-F0-9]{16}$'))
        putParse.add_argument('vlan', required=False, location='form', action='append',
                                nullable=False, type=inputs.regex(r'^[A-Za-z0-9]{1,32}$'))
        putParse.add_argument('expiry', required=False, location='form', type=float)
        auth = self.auth_test({}, request.cookies, '') # test auth
        args = putParse.parse_args()
        if auth != True:
            return auth
        user = jwt.decode(request.cookies['token'], self.auth_secret, algorithm='HS256').get('user')
        record = self.keys.find_one({'user': user, 'keyphrase': args['keyphrase']})# check key exists for that user
        if record is None:
            return {'token': None}, 404
        record_data = None
        token_data = {'key': args['keyphrase'],
                'nbf': datetime.utcnow(), # Not usable before now
                'iat': datetime.utcnow()} # Issued at
        if args['expiry'] != None and args['expiry'] >= 0:
            if args['expiry'] == 0:
                record_data = {'expiry': 0}
            else:
                start_time = jwt.decode(request.cookies['token'], self.auth_secret, algorithm='HS256').get('iat')
                end_time = datetime.fromtimestamp(start_time) + timedelta(hours=args['expiry'])
                token_data['exp'] = end_time # Add expiry to token
                record_data = {'expiry': end_time.timestamp()}
        elif record['expiry'] > 0:
            token_data['exp'] = datetime.fromtimestamp(record['expiry']) # Add expiry to token
        if args['vlan'] is not None:
            record_data = {'vlan': args['vlan']}
        if record_data:
            self.keys.update_one({'user': user, 'keyphrase': args['keyphrase']}, {'$set': record_data}) # update record
        token = jwt.encode(token_data, self.auth_secret, algorithm='HS256').decode("utf-8") # generate new key
        return {'auth-token': token}, 201

    def delete(self):
        delParse = reqparse.RequestParser()
        delParse.add_argument('keyphrase', required=True, location='form',
                                nullable=False, type=inputs.regex(r'^[A-F0-9]{16}$'))
        delParse.add_argument('confirm', required=True, location='form', choices=['true'])
        auth = self.auth_test({}, request.cookies, '') # test auth
        args = delParse.parse_args()
        if auth != True:
            return auth
        user = jwt.decode(request.cookies['token'], self.auth_secret, algorithm='HS256').get('user')
        record = self.keys.find_one({'user': user, 'keyphrase': args['keyphrase']})# check key exists for that user
        if record is None:
            return {'token': None}, 404
        result = self.keys.delete_one({'user': user, 'keyphrase': args['keyphrase']}) # delete record
        if result.deleted_count != 1:
            return {'success': False},500
        return {'success': True},201


class Auth:
    """Wrapper class for handling request authentication"""

    def __init__(self, db, secret):
        self.users = db.users
        self.keys = db.keys
        self.auth_secret = secret

    def auth_test(self, headers, cookies, vlan):
        api_key = headers.get('auth-token') # get key from auth-token header
        if api_key is not None:
            try: # verify and decode token
                keyphrase = jwt.decode(api_key, self.auth_secret, algorithm='HS256')['key']
            except jwt.exceptions.ExpiredSignatureError:
                return {'message': 'invalid API key'}, 403
            except (jwt.exceptions.InvalidTokenError, KeyError):
                return {'message': 'invalid API key'}, 500
            record = self.keys.find_one({'keyphrase': keyphrase}) # retrieve record from keys
            if vlan in record.get('vlan'): # test if key has access to vlan
                return True
        user_key = cookies.get('token') # get user from token cookie
        if user_key is not None:
            try: # verify and decode token
                user = jwt.decode(user_key, self.auth_secret, algorithm='HS256')['user']
            except jwt.exceptions.ExpiredSignatureError:
                return {'message': 'invalid user key'}, 403
            except (jwt.exceptions.InvalidTokenError, KeyError):
                return {'message': 'invalid user key'}, 500
            if self.users.count({'user': user}): # test if user exists in users
                return True
        return {'message': 'unauthorised'}, 403
