# Ubuntu Install

Update Ubuntu Packages:
```
sudo apt update
```
Create User
```commandline
user add hut-admin
usermod -aG sudo hut-admin
```

Install HTTPS Comms
```
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
```

Install Nginx Server
```
curl -1sLf 'https://dl.cloudsmith.io/public/caddy... | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy... | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```

Install Python 3
```
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-venv
```

Clone GitHub Repo for Interface App
```
sudo apt install git
git clone REPO
```

Install NMAP
```commandline
apt-get install nmap
```

Install Requirements 
```commandline 
pip install virtualenv
python -m venv venv
venv/bin/activate  LINUX
pip isntall -r requirements.txt
```

```commandline Initial Commands
flask shell
db.create_all() 
```

#### Automatic Start (OnStartUp)
For autometic startup do the following
<ol> 
    <li>Run the Startup File for Windows or Linux</li>
    <li>Stop Services</li>
    <li>Check for Github Updates</li>
    <li>Download Updates</li>
    <li>Set Timer for Next Restart</li>
    <li>Have a Socket Open For Operations</li>
</ol>


# Windows Install

Install NMAP

Install IIS
-INSTALL IIS from Control Panel
-Install CGI Module Under IIS/applicationDevelopmet/CGI


Python Setup 
```commandline
FROM CMD
Install GIT
pip install virtualenv
python -m venv venv
C:\hut\venv\Scripts\activate.bat 
pip install -r requirements.txt
wfastcgi-enable
```

On Root - Fast CGI Settings:
Full Path (venv): C:\hut\venv\Scripts\python.exe
Arguments (venv): C:\hut\venv\Lib\site-packages\wfastcgi.py


Adding a Site in IIS:
Sitename: HUT-INTERFACE
Physical Path: C:\inetpub\wwwroot\hut
Binding: Http:IP:80

Handeler Mapping(Sites)
-Add module Mapping
 : request path: *
 : Module: FastCgiModule
 : Executable: c:\hut\venv\Scripts\python.exe|c:\hut\venv\Lib\site-packages\wfastcgi.py
 : Request Restrictons and Uncheck Box
 : Ok OK then No


IUSR and IIS_IUSRS Permisions to:
c:\hut
and Main Python Script



```commandline Run From venv
flask shell
db.create_all() 
```

  


