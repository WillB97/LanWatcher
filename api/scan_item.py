from flask import request
from flask_restful import reqparse, Resource, inputs
import pymongo


class ip_endpoint(Resource):
    """Configure in-depth information by IP address"""

    def __init__(self, db, auth):
        self.db = db
        self.auth_test = auth.auth_test

    def get(self, vlan, ip):
        if 'vlan_' + vlan not in self.db.collection_names(): # test vlan exists
            return {'error': "vlan does not exist"}, 404
        auth = self.auth_test(request.headers, request.cookies, vlan) # test auth
        if auth != True:
            return auth
        record = self.db['vlan_' + vlan].find({'ip': ip},{'_id': 0,'ip':0}, sort=[('mac',pymongo.ASCENDING)])
        if record.count() == 0:
            return {'error': "IP address not found"}, 404
        return {'ip': list(record)}

    def put(self, vlan, ip):
        putParse = reqparse.RequestParser()
        putParse.add_argument('mac', required=True, location='form',
                            nullable=False, type=inputs.regex(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$'))
        putParse.add_argument('name', required=True, location='form', nullable=False)
        args = putParse.parse_args()
        if 'vlan_' + vlan not in self.db.collection_names(): # test vlan exists
            return {'error': "vlan does not exist"}, 404
        auth = self.auth_test(request.headers, request.cookies, vlan) # test auth
        if auth != True:
            return auth
        record = self.db['vlan_' + vlan].find_one({'mac': args['mac'], 'ip': ip},{'_id': 0}) # test record exists
        if record is None:
            return {'error': "MAC/IP address pair not found"}, 404
        result = self.db['vlan_' + vlan].update_one({'mac': args['mac'], 'ip': ip},
                        {'$set': {'name': args['name']}})
        if result.modified_count != 1:
            return {'success': False}, 500
        return {'success': True}, 201

    def delete(self, vlan, ip):
        delParse = reqparse.RequestParser()
        delParse.add_argument('mac', required=True, location='form',
                            nullable=False, type=inputs.regex(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$'))
        delParse.add_argument('confirm', required=True, location='form', nullable=False, choices=['true'])
        args = delParse.parse_args()
        if 'vlan_' + vlan not in self.db.collection_names(): # test vlan exists
            return {'error': "vlan does not exist"}, 404
        auth = self.auth_test(request.headers, request.cookies, vlan) # test auth
        if auth != True:
            return auth
        record = self.db['vlan_' + vlan].find_one({'mac': args['mac'], 'ip': ip},{'_id': 0}) # test record exists
        if record is None:
            return {'error': "MAC/IP address pair not found"}, 404
        result = self.db['vlan_' + vlan].delete_one({'mac': args['mac'], 'ip': ip})
        if result.deleted_count != 1:
            return {'success': False}, 500
        return {'success': True}, 201


class mac_endpoint(Resource):
    """Configure in-depth information by MAC address"""

    def __init__(self, db, auth):
        self.db = db
        self.auth_test = auth.auth_test

    def get(self, vlan, mac):
        if 'vlan_' + vlan not in self.db.collection_names(): # test vlan exists
            return {'error': "vlan does not exist"}, 404
        auth = self.auth_test(request.headers, request.cookies, vlan) # test auth
        if auth != True:
            return auth
        record = self.db['vlan_' + vlan].find_one({'mac': mac}, {'_id': 0, 'mac': 0})
        if record is None:
            return {'error': "MAC address not found"}, 404
        return record

    def put(self, vlan, mac):
        putParse = reqparse.RequestParser()
        putParse.add_argument('name', required=True, location='form', nullable=False)
        args = putParse.parse_args()
        if 'vlan_' + vlan not in self.db.collection_names(): # test vlan exists
            return {'error': "vlan does not exist"}, 404
        auth = self.auth_test(request.headers, request.cookies, vlan) # test auth
        if auth != True:
            return auth
        record = self.db['vlan_' + vlan].find_one({'mac': mac},{'_id': 0}) # test record exists
        if record is None:
            return {'error': "MAC address not found"}, 404
        result = self.db['vlan_' + vlan].update_one({'mac': mac},{'$set': {'name': args['name']}})
        if result.modified_count != 1:
            return {'success': False}, 500
        return {'success': True}, 201

    def delete(self, vlan, mac):
        delParse = reqparse.RequestParser()
        delParse.add_argument('confirm', required=True, location='form', nullable=False, choices=['true'])
        delParse.parse_args()
        if 'vlan_' + vlan not in self.db.collection_names(): # test vlan exists
            return {'error': "vlan does not exist"}, 404
        auth = self.auth_test(request.headers, request.cookies, vlan) # test auth
        if auth != True:
            return auth
        record = self.db['vlan_' + vlan].find_one({'mac': mac},{'_id': 0}) # test record exists
        if record is None:
            return {'error': "MAC address not found"}, 404
        result = self.db['vlan_' + vlan].delete_one({'mac': mac})
        if result.deleted_count != 1:
            return {'success': False}, 500
        return {'success': True}, 201


class host_endpoint(Resource):
    """Configure in-depth information by hostname"""

    def __init__(self, db, auth):
        self.db = db
        self.auth_test = auth.auth_test

    def get(self, vlan, host):
        if 'vlan_' + vlan not in self.db.collection_names(): # test vlan exists
            return {'error': "vlan does not exist"}, 404
        auth = self.auth_test(request.headers, request.cookies, vlan) # test auth
        if auth != True:
            return auth
        record = self.db['vlan_' + vlan].find_one({'hostname': host},{'_id': 0, 'hostname':0})
        if record is None:
            return {'error': "hostname not found"}, 404
        return record

    def put(self, vlan, host):
        putParse = reqparse.RequestParser()
        putParse.add_argument('name', required=True, location='form', nullable=False)
        args = putParse.parse_args()
        if 'vlan_' + vlan not in self.db.collection_names(): # test vlan exists
            return {'error': "vlan does not exist"}, 404
        auth = self.auth_test(request.headers, request.cookies, vlan) # test auth
        if auth != True:
            return auth
        record = self.db['vlan_' + vlan].find_one({'hostname': host},{'_id': 0}) # test record exists
        if record is None:
            return {'error': "hostname not found"}, 404
        result = self.db['vlan_' + vlan].update_one({'hostname': host},{'$set': {'name': args['name']}})
        if result.modified_count != 1:
            return {'success': False}, 500
        return {'success': True}, 201

    def delete(self, vlan, host):
        delParse = reqparse.RequestParser()
        delParse.add_argument('confirm', required=True, location='form', nullable=False, choices=['true'])
        delParse.parse_args()
        if 'vlan_' + vlan not in self.db.collection_names(): # test vlan exists
            return {'error': "vlan does not exist"}, 404
        auth = self.auth_test(request.headers, request.cookies, vlan) # test auth
        if auth != True:
            return auth
        record = self.db['vlan_' + vlan].find_one({'hostname': host},{'_id': 0}) # test record exists
        if record is None:
            return {'error': "hostname not found"}, 404
        result = self.db['vlan_' + vlan].delete_one({'hostname': host})
        if result.deleted_count != 1:
            return {'success': False}, 500
        return {'success': True}, 201
