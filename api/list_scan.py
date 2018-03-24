from flask import request
from flask_restful import reqparse, Resource, inputs
import re
import pymongo


class scan_endpoint(Resource):
    """VLAN level overview"""

    def __init__(self, db, auth):
        self.db = db
        self.auth_test = auth.auth_test

    def get(self):
        auth = self.auth_test({}, request.cookies, '') # test auth
        if auth != True:
            return auth
        collections = self.db.collection_names()
        names = []
        for collection in collections:
            if re.findall(r'^vlan_', collection):
                names.append(re.findall(r'^vlan_(.*)$', collection)[0])
        return {'vlan': names}

    def post(self):
        postParse = reqparse.RequestParser()
        postParse.add_argument('vlan', required=True, location='form',
                                nullable=False, type=inputs.regex(r'^[A-Za-z0-9 ]{1,32}$'))
        auth = self.auth_test({}, request.cookies, '') # test auth
        args = postParse.parse_args()
        if auth != True:
            return auth
        if args['vlan'] in self.db.collection_names(): # test vlan doesn't already exist
            return {'error': 'VLAN already exists'}, 400
        self.db.create_collection('vlan_' + args['vlan']) # create collection
        self.db['vlan_' + args['vlan']].create_index([('last-seen', pymongo.DESCENDING)]) # add mac and last-seen indexes
        self.db['vlan_' + args['vlan']].create_index([('mac', pymongo.DESCENDING)], unique=True)
        return {'success': True}, 201


class vlan_endpoint(Resource):
    """Configure a VLAN's settings"""

    def __init__(self, db, auth):
        self.db = db
        self.auth_test = auth.auth_test

    def get(self, vlan):
        # test auth
        # test vlan exists
        # fetch all of a vlan
        # format data
        # return data
        pass

    def post(self, vlan):
        # test auth
        # validate arguments
        # test record doesn't exist
        # insert record
        # return success
        pass

    def put(self, vlan):
        pass

    def delete(self, vlan):
        # test auth
        # confirm deletion
        # test collection exists
        # drop collection
        # return success
        pass
