import json
from flask import Flask
from flask_restful import Api
from pymongo import MongoClient
from authentication import login_endpoint, keys_endpoint, Auth
from list_scan import scan_endpoint, vlan_endpoint
from scan_item import ip_endpoint, mac_endpoint, host_endpoint, manage_endpoint
app = Flask(__name__)
api = Api(app)

try:
    with open('config.json') as fs:
        config = json.load(fs)
except:
    raise

client = MongoClient(username=config.get('user'), password=config.get('pwd'), authSource='LanScan')
db = client['LanScan']

auth_help = Auth(db, config.get('secret'))

api.add_resource(login_endpoint, '/api/1.0/login', resource_class_args=(db, config.get('secret'), auth_help))
api.add_resource(keys_endpoint, '/api/1.0/token', resource_class_args=(db, config.get('secret'), auth_help))
api.add_resource(scan_endpoint, '/api/1.0/scans', resource_class_args=(db, auth_help))
api.add_resource(vlan_endpoint, '/api/1.0/scans/<vlan>', resource_class_args=(db, auth_help))
api.add_resource(ip_endpoint, '/api/1.0/scans/<vlan>/ip/<ip>', resource_class_args=(db, auth_help))
api.add_resource(mac_endpoint, '/api/1.0/scans/<vlan>/mac/<mac>', resource_class_args=(db, auth_help))
api.add_resource(host_endpoint, '/api/1.0/scans/<vlan>/host/<host>', resource_class_args=(db, auth_help))
api.add_resource(manage_endpoint, '/api/1.0/scans/<vlan>/manage', resource_class_args=(db, auth_help))

#fix for flask being behind a proxy
#from werkzeug.contrib.fixers import ProxyFix

#app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
