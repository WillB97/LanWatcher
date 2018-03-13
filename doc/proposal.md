Mongo and flask restful/restplus

Collection for each vlan and subnet

## DB Schema
Collection `vlan_<X>`
```
{
    "mac": <mac-address>,
    "ip": [<address>],
    "hostname": <hostname>,
    "last-seen": <unix-time>,
    "uptime": <minutes>,
    "name": <name>
}
```

Collection `users`
```
{
    "user": <str>,
    "pass": <salted hash>,
    "salt": <random string>
}
```

Collection `keys`
```
{
    "keyphrase": <str>,
    "vlan": [],
    "user": <_id>,
    "expiry": <unix time>
}
```

`/api/1.0/scans`
- view monitored vlans (get)
- create a new vlans (post)
    + set vlan name
`/api/1.0/scans/<vlan>`
- view current ip, hostname pairs (get)
    + filter timeframe
- manually add device (post)
    + mac, ip [, host][, seen][, name]
- upload scan data (put)
    + list with dict of data for each captured device
- remove vlans (delete)
    + confirm deletion
`/api/1.0/scans/<vlan>/ip/<ip host segment>`
- lookup in-depth information by IP (get)
- manually rename device by IP (put)
    + new name
- remove device (delete)
    + confirm deletion
`/api/1.0/scans/<vlan>/mac/<mac address>`
- lookup in-depth information by MAC (get)
- manually rename device by MAC (put)
    + new name
- remove device (delete)
    + confirm deletion
`/api/1.0/scans/<vlan>/host/<hostname>`
- lookup in-depth information by hostname (get)
- manually rename device by hostname (put)
    + new name
- remove device (delete)
    + confirm deletion
`/api/1.0/login`
- generate auth token (post)
    + send user and password creds
- alter user creds (put)
    + new password
`/api/1.0/token`
- list active API keys (get)
- generate API keys (post)
    + expiry
    + allowed VLANS
- alter API keys (put)
    + add VLAN
    + remove VLAN
    + alter expiry
- remove API key (delete)
    + key id
    + confirm deletion
