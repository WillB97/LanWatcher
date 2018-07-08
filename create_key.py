import requests
import json

base_url = input("Enter API URL (e.g. http://localhost:8080):")
print(base_url + '/api/1.0/login')
user = input("Enter username:")
password = input("Enter password:")

try:
	r = requests.post(base_url + '/api/1.0/login', data={'username':user,'password':password})
except:
	print("Failed to login as " + user + " at " + base_url)
	exit(-1)
if r.status_code != 200:
	print("Failed to login as " + user + " at " + base_url)
	exit(-1)
else:
	print("Successfully logged in to " + base_url + " as " + user)
	token = r.json()

vlan = input("Enter VLAN name:")

r = requests.post(base_url + '/api/1.0/scans', data={'vlan':[vlan]}, cookies=token)
if r.status_code != 201:
	print(r.text)
	if r.json().get('error') == 'VLAN already exists':
		print("VLAN " + vlan + " exists")
	else:
		print("Failed to create VLAN '" + vlan + "'")
		exit(-2)
else:
	print("Successfully created VLAN '" + vlan + "'")

expiry = input("Enter expiry UNIX time:")

r = requests.post(base_url + '/api/1.0/token', data={'vlan':vlan,'expiry':expiry}, cookies=token)
if r.status_code != 201:
	print("Failed to create API token for " + user)
	exit(-3)
else:
	print("Successfully created API token for " + user)
	print("API token: " + r.json()['auth-token'])
	api_token = r.json()['auth-token']

choice = input("Create scanrc [Y/N]")

if choice == 'Y' or choice == 'y':
	ip_range = input("Enter IP range in CIDR notation (e.g. 192.168.0.0/24):")
	with open('scanrc','w') as fs:
		json.dump({"ip_range": ip_range, "vlan": vlan, "key": api_token, "url": base_url}, fs, indent="\t")
	print("Move scanrc to the scanner directory and rename to .scanrc")