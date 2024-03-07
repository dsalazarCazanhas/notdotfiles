import subprocess
import datetime
import os
import time


packages = ['zip', 'unzip', 'alacritty-git', 'tmux-git', 'git', 'oh-my-zsh-git',
 'shadowsocks-git', 'dbus-glib', 'nmap-git', 'wireshark-git', 'virtualbox-bin',
  'virtualbox-bin-guest-iso', 'virtualbox-host-modules-arch']
cybersec_path = "/user/share/cybersec"
# Paru -Sw packages download only
current_dir = os.path.abspath(os.path.curdir())
home_path = os.getenv('HOME')
config_dir = f"{home_path}/.config"


# First, install paru
def install_paru():
    time.sleep(1)
    try:
        os.system("git clone https://aur.archlinux.org/paru-bin /tmp/paru && cd /tmp/paru; makepkg -sic")
        return True
    except:
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

def set_tor():
    time.sleep(1)
    try:
        os.system("paru -S proxychains tor torsocks")
        return True
    except:
        return False
    
def check_process_status(process_name):
    try:
        subprocess.check_output(["pgrep", process_name])
        return True
    except subprocess.CalledProcessError:
        return False

def download_packages():
    os.system("sudo systemctl restart tor")
    if check_process_status('tor'):
        try:
            subprocess.run(["proxychains4", "paru", "-Sw", "--noconfirm"] + packages)
            return True
        except subprocess.CalledProcessError:
            return False
    else:
        pass

def install_packages():
    if download_packages:
        try:
            subprocess.run(["paru", "-S", "--noconfirm", "--needed", "--sudoloop"] + packages)
        except subprocess.CalledProcessError:
            return False
    else:
        pass

def main():
    print("Installing...")
    time.sleep(1)
    print("Preparing folders")
    os.system(f"sudo mkdir /usr/share/cybersec && sudo chown {os.getenv('UID')}:{os.getenv('GID')} /usr/share/cybersec")
    time.sleep(2)
    print("Installing ohmyzsh")
    ohmyzsh()
    print("Installing FZF")
    install_fzf()
    time.sleep(2)
    print("Setting commix, cyberchef and tor-browser")
    os.system(f"git clone https://github.com/commixproject/commix.git {cybersec_path}/commix")
    print("Downloading cyberchef")
    os.system(f"mkdir {cybersec_path}/cyberchef")
    os.system(f"curl https://gchq.github.io/CyberChef/CyberChef_v10.8.2.zip -o {cybersec_path}/cyberchef/cyber.zip")
    os.system(f"cd {cybersec_path}/cyberchef && unzip cyber.zip")
    print("Downloading paru")
    if  install_paru:
        set_tor()
        print("Packages downloaded, lets install them...")
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

