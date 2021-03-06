## VLAN management

URI: `/api/1.0/scans`

#### GET
List VLANs currently monitored
```
args: {},
response: {
    "vlan": [
        < alphanumeric >
    ]
}, 200
```

#### POST
Setup a new VLAN to be monitored
```
args: {
    "vlan": < alphanumeric >
},
response: {
    "success": True
}, 201
```

---

## Scan management
curl -H "auth-token:$auth" localhost:8080/api/1.0/scans/test
URI: `/api/1.0/scans/<vlan>`

#### GET
List data stored about each occupied IP address
```
args: {
    "to": < int(unix time) >,   // Optional
    "from": < int(unix time) >  // Optional
},
response: {
    < IP address > : {
        "mac": < MAC address >,
        "hostname": < FQDN >,
        "name": < string >
    },
    ...
}, 200
```

#### POST
Manually insert additional devices
```
args: {
    "mac": < mac address >,
    "ip": < IP address >,
    "ip": ...,
    "host": < FQDN >,
    "seen": < float(unix time) >
},
response: {
    "success": True
}, 201
```

#### PUT
Upload bulk device data generated by the scanning script
```
json: [
    {
        "hostname": < FQDN >,
        "ip": [
            < IP address >
        ],
        "last-seen": < int(unix time) >,
        "mac": < MAC address >
    }
],
response: {
    'updated': < int >,
    'inserted': < int >
}, 201
```

#### DELETE
Delete a VLAN's monitoring data
```
args: {
    "confirm": "true"
},
response: {
    "success": True
},201
```
