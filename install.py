import subprocess
import datetime
import os
import time


packages = ['zip', 'unzip', 'alacritty-git', 'tmux-git', 'git', 'oh-my-zsh-git',
 'shadowsocks-git', 'dbus-glib', 'nmap-git', 'wireshark-git', 'virtualbox-bin',
  'virtualbox-bin-guest-iso', 'virtualbox-host-modules-arch']
cybersec_path = "/user/share/cybersec"
# Paru -Sw packages download only
current_dir = os.path.abspath(os.path.curdir)
home_path = subprocess.run(['echo', '$HOME'], check=True)
config_dir = f"{home_path}/.config"
cur_user = subprocess.run(['echo', '$USER'], check=True)
cur_user_uid = int(subprocess.check_output(['id', '-u']))
cur_user_gid = int(subprocess.check_output(['id', '-g']))

# First, install paru
def install_paru():
    time.sleep(2)
    try:
        subprocess.run(['git', 'clone', 'https://aur.archlinux.org/paru-bin', '/tmp/paru', '&&', 
        'cd','/tmp/paru', ';', 'makepkg', '-sic'])
        return True
    except:
        raise Exception("Problema con tu primo el paru")
        return False

def set_tor():
    time.sleep(1)
    try:
        subprocess.run(['paru', '-S', 'proxychains tor torsocks'])
        return True
    except:
        raise Exception("Problemas en el metodo set tor")
        return False

def install_oh_my_zsh():
    time.sleep(1)
    try:
        os.system("sh -c '$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)'")
        return True
    except:
        return False

def install_fzf():
    try:
        os.system("git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf && ~/.fzf/install")
        return True
    except:
        return False
    
def check_process_status(String: process_name):
    try:
        subprocess.check_output(['pgrep', process_name])
        return True
    except subprocess.CalledProcessError:
        raise Exception("This process is not running")
        return False

def download_packages():
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'tor'])
    except:
        print("Tor isn't running")
        return 1
    if check_process_status('tor'):
        try:
            subprocess.run(["proxychains4", "paru", "-Sw", "--noconfirm"] + packages, check=True)
            return True
        except subprocess.CalledProcessError:
            raise Exception("There was an error downloading packages")
            return 1
    else:
        raise Exception("There is a problem with tor process")
        return 1

def install_packages():
    if download_packages():
        try:
            subprocess.run(["paru", "-S", "--noconfirm", "--needed", "--sudoloop"] + packages, check=True)
        except subprocess.CalledProcessError:
            raise Exception("There was a problem installing packages")
            return 1
    else:
        raise Exception("There is an error on download_packages function")
        return 1

def main():
    print("Installing...")
    time.sleep(1)
    print("Preparing folders...")
    time.sleep(2)
    try:
        subprocess.run(['sudo', 'mkdir', '/usr/share/cybersec'], check = True)
        subprocess.run(['sudo', 'chown', '{cur_user_uid}:{cur_user_gid}', '/usr/share/cybersec'], check = True)
        return 0
    except subprocess.CalledProcessError:
        raise Exception(f"There was an error executing sudo")
        exit
    time.sleep(2)
    #print("Installing ohmyzsh")
    #install_oh_my_zsh()
    #print("Installing FZF")
    #install_fzf()
    #time.sleep(2)
    #print("Setting commix, cyberchef and tor-browser")
    #os.system(f"git clone https://github.com/commixproject/commix.git {cybersec_path}/commix")
    #print("Downloading cyberchef")
    #os.system(f"mkdir {cybersec_path}/cyberchef")
    #os.system(f"curl https://gchq.github.io/CyberChef/CyberChef_v10.8.2.zip -o {cybersec_path}/cyberchef/cyber.zip")
    #os.system(f"cd {cybersec_path}/cyberchef && unzip cyber.zip")
    print("Downloading paru")
    if  install_paru():
        #set_tor()
        print("Packages downloaded, lets install them...")
        exit
        time.sleep(2)
        install_packages()
        print("Finished...")
    else:
        print("There is an error somewhere, somehow")
    time.sleep(2)
    print("Setting configuration files...")
    os.system(f"cp -rf zsh_powerlevel/p10k.zsh {home_path}/.p10k.zsh;"
        f"cp -rf zsh_powerlevel/zshrc {home_path}/.zshrc;"
        f"cp -rf config/alacritty.toml {home_path}/.alacritty.toml;"
        f"cp -rf config/tmux.conf {home_path}/.tmux.conf;"
        f"cp -rf config/nvim {config_dir}")
    os.system(f"cp -fr fonts {config_dir} && cd {config_dir}/fonts/Hack && unzip Hack.zip && fc-cache -fv")
    
    time.sleep(2)
    return "FINISHED maybe..."

# Start script #
if ( cur_user == 'root'):
	raise Exception("This script can't be run as root")
else:
    print("Starting...")
    try:
        main()
    except:
        raise Exception("Something went wrong")

