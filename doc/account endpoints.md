## Account Management

URI: `/api/1.0/login`

#### POST
Generate user authentication token from credentials
```
args: {
    "username": < alphanumeric >,
    "password": < string >
},
response: {
    "token": < jwt token >
}, 200
```

#### PUT
Change the authenticated user's password
```
args: {
    "password": < string >
},
response: {
    "success": True
}, 201
```

---

## API Key Management

URI: `/api/1.0/token`

#### GET
List the API keys associated with the authenticated user
```
args: {},
response: {
    "data": [
        "keyphrase": < hexadecimal >,
        "vlan": [
            < alphanumeric >
        ],
        "expiry": < float(unix time) | 0 >
    ]
}, 200
```

#### POST
Generate a new API key and associate it with the authenticated user
```
args: {
    "expiry": < float(unix time) >,
    "vlan": < alphanumeric >,
    "vlan": ...
},
response: {
    "token": < jwt token >,
    "keyphrase": < hexadecimal >
}, 201
```

#### PUT
Alter a pre-existing API key, add and remove VLANs and expiry.
```
args: {
    "keyphrase": < alphanumeric >,
    "expiry": < float(unix time) >, // Optional
    "vlan": < alphanumeric >,     // Optional
    "vlan": ...                   // Optional
},
response: {
    "token": < jwt token >
}, 201
```

#### DELETE
Remove an API key associated with the authenticated user
```
args: {
    "keyphrase": < hexadecimal >,
    "confirm": "true"
},
response: {
    "success": True
}, 201
```
