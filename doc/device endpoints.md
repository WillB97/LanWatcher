## IP Management

URI: `/api/1.0/scans/<vlan>/ip/<ip>`

#### GET
Lookup in-depth device information by IP address
```
args: {},
response: {
    "ip": [
        "mac": < MAC address >,
        "hostname": < FQDN >,
        "last-seen": < float(unix time) >,
        "name": < string >
    ]
}, 200
```
#### PUT
Name device by IP/MAC address pair
```
args: {
    "mac": < MAC address >,
    "name": < string >
},
response: {
    "success": True
}, 201
```
#### DELETE
Delete device by IP/MAC address pair
```
args: {
    "mac": < MAC address >,
    "confirm": "true"
},
response: {
    "success": True
}, 201
```

---

## MAC Address Management

URI: `/api/1.0/scans/<vlan>/mac/<mac>`

#### GET
Lookup in-depth device information by MAC address
```
args: {},
response: {
    "hostname": < string >,
    "ip": [
        < IP address >
    ],
    "last-seen": < float(unix time) >,
    "name": < string >
}, 200
```
#### PUT
Name device by MAC address
```
args: {
    "name": < string >
},
response: {
    "success": True
}, 201
```
#### DELETE
Delete device by MAC address
```
args: {
    "confirm": "true"
},
response: {
    "success": True
}, 201
```

---

## Hostname Management

URI: `/api/1.0/scans/<vlan>/host/<hostname>`

#### GET
Lookup in-depth device information by hostname
```
args: {},
response: {
    "mac": < MAC address >,
    "ip": [
        < IP address >
    ],
    "last-seen": < float(unix time) >,
    "name": < string >
}, 200
```
#### PUT
Name device by hostname
```
args: {
    "name": < string >
},
response: {
    "success": True
}, 201
```
#### DELETE
Delete device by hostname
```
args: {
    "confirm": "true"
},
response: {
    "success": True
}, 201
```

---

## Scan Management

URI: `/api/1.0/scans/<vlan>/manage`

#### POST
Toggle uptime being counted
```
args:{
    "enabled": < boolean >
},
response:{
    "success": True
},201
```
#### PUT
Set the maximum time between seeing nodes without downtime being recorded
```
args: {
    "max-time": < int >
},
response: {
    "success": True
}, 201
```
#### DELETE
Delete ip records in a time range
```
args: {
    "older": < float(unix time) >,
    "newer": < float(unix time) >,
    "confirm": "true"
},
response: {
    "deleted": < int >
}, 201
```