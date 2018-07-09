#! /bin/bash
# Check for root
if [ "$(id -u)" -ne 0 ]; then
	printf 'This script must be run as root. Using sudo...\n' "$(basename "$0")" >&2
	exec sudo -k -- /bin/sh "$0" "$@" || exit -1
fi

# Get original user
normal_user="${SUDO_USER-$(who -m | awk '{print $1}')}"

apt-get install nginx -y
pip3 install gunicorn

cat > wsgi.py <<- EOF
from API_base import app

if __name__ == "__main__":
    app.run()
EOF

chown $normal_user:www-data wsgi.py

cat > /etc/systemd/system/gunicorn.service <<- EOF
[Unit]
Description=Gunicorn instance to serve LanWatcher
After=network.target

[Service]
User=$normal_user
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind unix:lanwatcher.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/nginx/sites-available/lanwatcher <<- EOF
server {
    listen 80;
    server_name $(hostname -f);

    location / {
        include proxy_params;
        proxy_pass http://unix:$(pwd)/lanwatcher.sock;
    }
}
EOF

chown -R :www-data ../api 
systemctl daemon-reload
systemctl start gunicorn
systemctl enable gunicorn
ln -s /etc/nginx/sites-available/lanwatcher /etc/nginx/sites-enabled
rm /etc/nginx/sites-enabled/default
nginx -s reload
