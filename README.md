REST API to keep track of occupied IP addresses on a network
- Multi-network support
- Detached scanner to allow monitoring of networks without the webserver being on the network

### Installation:
```bash
sudo apt-get update
sudo apt-get install python3.5-pip -y
pip3 install --user -U -R requirements.txt
```

### Usage (Network Scanner):
```bash
python3.5 nmap_scan.py 192.168.0.0/24
```