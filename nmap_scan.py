import pprint 
import json
from datetime import datetime
import subprocess
import sys
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from ipaddress import ip_network

def nmap_scan(ipRange):
    p = subprocess.Popen(['sudo','nmap','-oX','-','-sn','-R',ipRange],
                                bufsize=10000,stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (temp_xml,temp_err) = p.communicate()
    temp_json=bf.data(fromstring(temp_xml))

    timeNow = datetime.now().strftime("[%d/%m/%y %H:%M:%S]")
    print('Scan run at {} in {} seconds, hosts up: {} of {}'.format(timeNow,
                        temp_json['nmaprun']['runstats']['finished']['@elapsed'],
                        temp_json['nmaprun']['runstats']['hosts']['@up'],
                        temp_json['nmaprun']['runstats']['hosts']['@total']))

    if type(temp_json['nmaprun']['host']) != list:
        temp_json['nmaprun']['host'] = [ temp_json['nmaprun']['host'] ]

    pp = pprint.PrettyPrinter()
    timeval = int(datetime.utcnow().timestamp())
    data = []
    for y in range(0,temp_json['nmaprun']['runstats']['hosts']['@up']):
        device_data = {'ip':[]}

        device_data['hostname'] = temp_json['nmaprun']['host'][y]['hostnames'].get('hostname',{'@name':'undefined'})['@name']
        
        if type(temp_json['nmaprun']['host'][y]['address']) != list:
            temp_json['nmaprun']['host'][y]['address'] = [temp_json['nmaprun']['host'][y]['address']]

        # localhost exception
        if temp_json['nmaprun']['host'][y]['status']['@reason'] == 'localhost-response':
            # add local mac address
            pass

        # find address of type mac
        # make list of addresses type ipv4 or ipv6
        for x in temp_json['nmaprun']['host'][y]['address']:
            if x['@addrtype'] == 'mac':
                device_data['mac'] = x['@addr']
            elif x['@addrtype'] in ['ipv4','ipv6']:
                device_data['ip'].append(x['@addr'])
        device_data['last-seen'] = timeval
        data.append(device_data)

    pp.pprint(data)

scanRange = None
try:
    with open('.scanrc') as fs:
        configData = json.load(fs)
        scanRange = configData['ip_range']
        ip_network(scanRange, strict=False)
except FileNotFoundError:
    pass
except json.JSONDecodeError:
    print('Invalid config file', file=sys.stderr)
except ValueError:
    print('Invalid IP network in config', file=sys.stderr)
except KeyError:
    print('IP network not specified in config', file=sys.stderr)

if len(sys.argv) == 2:
    try:
        ip_network(sys.argv[1], strict=False)
        scanRange = sys.argv[1]
    except ValueError:
        print('Invalid IP network', file=sys.stderr)

if scanRange is None:
    print('Scan range missing', file=sys.stderr)
    exit()

nmap_scan(scanRange)