# Setup Guide
* ```sudo apt ```
* ```sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools```
* ```sudo apt install python3-venv```
* ```mkdir hoster``` (make sure you are in /home)
* ```cd hoster```
* ```python3.6 -m venv host```
* ```source host/bin/activate```
* ```pip install wheel```
* ```pip install uwsgi flask```
* wget and unzip this repo and extract the files out of the folder and into the "hoster" directory
* ```sudo nano /etc/systemd/system/host.service```
  * You only need to do this if you want to run it on another user than root, store it in another directory or changed the name of it.
* ```sudo systemctl start host```
* ```sudo systemctl enable host```
  * You can check the status of it with ```sudo systemctl status myproject```
* ```sudo apt-get install nginx```
* ```sudo nano /etc/nginx/sites-available/host```
```
server {
    listen 80;
    server_name your_domain www.your_domain;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/hoster/host.sock;
    }
}
```
* ```sudo ln -s /etc/nginx/sites-available/host /etc/nginx/sites-enabled```
  * ```sudo nginx -t``` to check for syntax errors
* ```sudo systemctl restart nginx```
* ```sudo ufw allow 'Nginx Full'```
* ```sudo add-apt-repository ppa:certbot/certbot```
* ```sudo apt install python-certbot-nginx```
* ```sudo certbot --nginx -d your_domain -d www.your_domain```
* Click 2 and press enter.
* ```sudo ufw delete allow 'Nginx HTTP'```

Source: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04
