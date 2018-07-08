from flask import request
from flask_restful import reqparse, Resource, inputs
import re
import pymongo
from datetime import datetime, timedelta
import ipaddress


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
                                nullable=False, type=inputs.regex(r'^[A-Za-z0-9]{1,32}$'))
        auth = self.auth_test({}, request.cookies, '') # test auth
        args = postParse.parse_args()
        if auth != True:
            return auth
        if 'vlan_' + args['vlan'] in self.db.collection_names(): # test vlan doesn't already exist
            return {'error': 'VLAN already exists'}, 400
        self.db.create_collection('vlan_' + args['vlan']) # create collection
        # add mac and last-seen indexes
        self.db['vlan_' + args['vlan']].create_index([('last-seen', pymongo.DESCENDING)])
        self.db['vlan_' + args['vlan']].create_index([('mac', pymongo.DESCENDING)], unique=True)
        return {'success': True}, 201


class vlan_endpoint(Resource):
    """Configure a VLAN's settings"""

    def __init__(self, db, auth):
        self.db = db
        self.auth_test = auth.auth_test

    def get(self, vlan):
        getParse = reqparse.RequestParser()
        getParse.add_argument('vlan', required=True, location='view_args', nullable=False)
        getParse.add_argument('to', required=False, location='args', type=int)
        getParse.add_argument('from', required=False, location='args', type=int)
        args = getParse.parse_args()
        if 'vlan_' + args['vlan'] not in self.db.collection_names(): # test vlan exists
            return {'error': "vlan does not exist"}, 404
        auth = self.auth_test(request.headers, request.cookies, args['vlan']) # test auth
        if auth != True:
            return auth
        find_filter = {}
        time_filter = {}
        if args['to'] is not None:
            time_filter['$lt'] = args['to']
        if args['from'] is not None:
            time_filter['$gt'] = args['from']
        if time_filter is not {}:
            find_filter = {'last-seen': time_filter}
        records = self.db['vlan_' + args['vlan']].find(find_filter,
                {'_id': 0, 'ip': 1, 'mac': 1, 'hostname': 1, 'name': 1}) # fetch all of a vlan
        result = {} # format data (dictionary by ip)
        for record in records:
            for ip in record['ip']:
                result[ip] = {k:v for k,v in record.items() if k not in ['ip']}
        return result

    def post(self, vlan):
        postParse = reqparse.RequestParser()
        postParse.add_argument('vlan', required=True, location='view_args', nullable=False)
        postParse.add_argument('mac', required=True, location='form', # validate arguments
                                nullable=False, type=inputs.regex(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$'))
        postParse.add_argument('ip', required=True, location='form', action='append',
                                nullable=False, type=inputs.regex(r'^[0-9A-F.:]+$'))
        postParse.add_argument('host', required=False, default='', location='form', nullable=False)
        postParse.add_argument('seen', required=False, default=0, location='form',
                                nullable=False, type=float)
        args = postParse.parse_args()
        try: # validate IP addresses
            for ip in args['ip']:
                ipaddress.ip_address(ip)
        except ValueError:
            return {'error': "invalid IP address"}, 400
        if 'vlan_' + args['vlan'] not in self.db.collection_names(): # test vlan exists
            return {'error': "vlan does not exist"}, 404
        auth = self.auth_test(request.headers, request.cookies, args['vlan']) # test auth
        if auth != True:
            return auth
        exists = self.db['vlan_' + args['vlan']].count({'mac': args['mac']}) # test record doesn't exist
        if exists:
            return {'error': 'device already exists'}, 400
        data = {
            "mac": args['mac'],
            "ip": args['ip'],
            "hostname": args['host'],
            "last-seen": (datetime.utcnow() - timedelta(hours=args['seen'])).timestamp(),
            "uptime": 0,
            "name": ""
        }
        self.db['vlan_' + args['vlan']].insert_one(data) # insert record
        return {'success': True}, 201

    def put(self, vlan):
        if 'vlan_' + vlan not in self.db.collection_names(): # test vlan exists
            return {'error': "vlan does not exist"}, 404
        auth = self.auth_test(request.headers, request.cookies, vlan) # test auth
        if auth != True:
            return auth
        if type(request.json) is not list:
            return {'error': "data must be in a list"}, 400
        records = []
        for device in request.json:
            if not device.get('mac') or not re.findall(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$', device.get('mac')): # validate mac
                continue
            try: # validate IP addresses
                for ip in device.get('ip'):
                    ipaddress.ip_address(ip)
            except ValueError:
                return {'error': "invalid IP address"}, 400
            if type(device.get('last-seen')) is not int: # last seen type
                continue
            if type(device.get('hostname')) is not str: # hostname isn't null
                device['hostname'] = ''
            record_data = {'$set': {
                "mac": device['mac'],
                "ip": device['ip'],
                "hostname": device['hostname'],
                "last-seen": device['last-seen']},
            '$setOnInsert': {
                'uptime': 0,
                'name': ""}
            }
            # TODO: calculate uptime
            records.append(pymongo.UpdateOne({'mac': device['mac']},
                            record_data, upsert=True)) # append records
        result = self.db['vlan_' + vlan].bulk_write(records, ordered=False) # execute bulk write
        return {'updated': result.modified_count, 'inserted': result.upserted_count}, 201 # return successful updates

    def delete(self, vlan):
        delParse = reqparse.RequestParser()
        delParse.add_argument('vlan', required=True, location='view_args', nullable=False)
        delParse.add_argument('confirm', required=True, location='form',
                                nullable=False, choices=['true']) # confirm deletion
        args = delParse.parse_args()
        if 'vlan_' + args['vlan'] not in self.db.collection_names(): # test vlan exists
            return {'error': "vlan does not exist"}, 404
        auth = self.auth_test({}, request.cookies, args['vlan']) # test auth
        if auth != True:
            return auth
        self.db['vlan_' + args['vlan']].drop() # drop collection
        return {'success': True}, 201
