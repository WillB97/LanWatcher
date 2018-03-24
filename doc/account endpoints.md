## Account Management

URI: `/api/1.0/login`

#### POST
Generate user authentication token from credentials
```
args: {
    "username": < string >,
    "password": < alphanumeric >
},
response: {
    "token": < jwt token >
}, 200
```

#### PUT
Change the authenticated user's password
```
args: {
    "password": < alphanumeric >
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
        "keyphrase": < alphanumeric >,
        "vlan": [
            < string >
        ],
        "expiry": < unix timestamp | 0 >
    ]
}, 200
```

#### POST
Generate a new API key and associate it with the authenticated user
```
args: {
    "expiry": < int >,
    "vlan": < string >,
    "vlan": ...
},
response: {
    "token": < jwt token >,
    "keyphrase": < alphanumeric >
}, 201
```

#### PUT
Alter a pre-existing API key, add and remove VLANs and expiry.
```
args: {
    "keyphrase": < alphanumeric >,
    "expiry": < int >,  // Optional
    "vlan": < string >, // Optional
    "vlan": ...         // Optional
},
response: {
    "token": < jwt token >
}, 201
```

#### DELETE
Remove an API key associated with the authenticated user
```
args: {
    "keyphrase": < alphanumeric >,
    "confirm": "true"
},
response: {
    "success": True
}, 201
```
