REST API to keep track of occupied IP addresses on a network
- Multi-network support
- Detached scanner to allow monitoring of networks without the webserver being on the network

### Installation (REST API)
```bash
sudo apt-get update
sudo apt-get install python3-pip git -y
pip3 --version
git clone https://github.com/WillB97/LanWatcher.git
pip3 install --user --upgrade pip
cd LanWatcher/api
pip3 install --user -U -r requirements.txt
sudo apt-get install mongodb -y
# setup the database admin and worker user and creates the default user (admin/admin)
python3 setup.py
```

In /etc/mongodb.conf:
```
auth = true
```

```bash
sudo service mongodb restart
# start temporary server
python3 API_base.py
sudo ./nginx_setup.sh
```

### Installation (Network Scanner):
```bash
sudo apt-get update
sudo apt-get install python3-pip nmap -y
git clone https://github.com/WillB97/LanWatcher.git
pip3 install --user --upgrade pip
cd LanWatcher
pip3 install --user -U -r requirements.txt
python3 create_key.py
# run initial scan
python3 nmap_scan.py
crontab -e
```

In crontab:
```
# scan LAN every 5 minutes
*/5 * * * * cd /home/will/LanWatcher && /usr/bin/python3 nmap_scan.py >/dev/null
# edit path for the location of the git directory
```

### Usage (Network Scanner):
```bash
python3 nmap_scan.py 192.168.0.0/24
```

#### To create API tokens
1. POST username and password to /api/1.0/login for an authorisation token, return the token as a cookie in all future requests
2. POST a VLAN name to /api/1.0/scans to set a VLAN up for monitoring
3. POST an expiry in unix time, and the VLANs it can be used in to /api/1.0/token for an API token, use 0 for a token that doesn't expire
