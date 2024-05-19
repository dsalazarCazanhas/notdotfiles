import subprocess
import os
import time

packages = ['zip', 'unzip', 'alacritty-git', 'tmux-git', 'git', 'oh-my-zsh-git',
            'shadowsocks-git', 'dbus-glib', 'nmap-git', 'wireshark-git', 'virtualbox-bin',
            'virtualbox-bin-guest-iso', 'virtualbox-host-modules-arch', 'diffutils',
            'util-linux', 'less', 'debugedit', 'fakeroot', 'gzip', 'binutils',
            'bat', 'devtools', 'lsd']
cybersec_path = "/user/share/cybersec"
# Paru -Sw packages download only
install_dir = os.path.dirname(__file__)
home_path = os.getenv('HOME')
config_dir = f"{home_path}/.config"
cur_user = subprocess.check_output(['id', '-un']).decode('utf-8')
cur_user_uid = int(subprocess.check_output(['id', '-u']))
cur_user_gid = int(subprocess.check_output(['id', '-g']))


def stop_on_error(excep: Exception, func_name: str):
    print(f"The program will stop because there was an error"
          f"on function '{func_name}' with error: {excep}")
    exit()


def reboot():
    print("All is up to date, a reboot is needed, consider it.\n "
          "I will create a cron file that will execute the script "
          "again after the reboot. So, reboot?")
    x = input("(x/y)").lower()
    if x == 'y':
        if subprocess.check_output(['crontab', '-V']):
            print('Cron is installed, lets go.')
            time.sleep(2)
            os.system(f"echo \"@reboot python {install_dir}/install.py | crontab -")
            os.system("sudo systemctl enable crontab; sudo systemctl start crontab && \
                sudo reboot")
        else:
            print("Crontab isn't installed, don't worry I'll take care")
            try:
                install_pkg('cronie')
                time.sleep(2)
                reboot()
            except Exception as e:
                stop_on_error(e, reboot.__name__)
    elif x == 'n':
        return True
    else:
        print("Plz type y or n.")
        reboot()


def install_pkg(pkg: str):
    try:
        subprocess.run(['sudo', 'pacman', '-S', pkg, '--noconfirm', '--needed'])
        return True
    except Exception as e:
        stop_on_error(e, install_pkg.__name__)


def check_process_status(process_name: str):
    try:
        subprocess.check_output(['pgrep', process_name])
        time.sleep(2)
        print(f"The process {process_name} is running, continuing")
        return True
    except subprocess.CalledProcessError:
        print(f"The process {process_name} is not running")
        return False


def init():
    time.sleep(2)
    print("Executing first system upgrade.")
    time.sleep(1)
    subprocess.run(['sudo', 'pacman-key', '--init'])
    subprocess.run(['sudo', 'pacman-key', '--populate'])
    try:
        subprocess.run(['sudo', 'pacman', '-Syyu', '--noconfirm'], check=True)
        time.sleep(3)
        reboot()
    except Exception as e:
        stop_on_error(e)


def install_paru():
    if subprocess.check_output(['git', '-v']):
        if subprocess.check_output(['paru', '-V']):
            print("Paru is already installed.")
            return True
        print("Git is installed, cloning paru...")
        time.sleep(2)
        try:
            subprocess.run(['git', 'clone', 'https://aur.archlinux.org/paru-bin', '/tmp/paru'])
            os.system("cd /tmp/paru; makepkg -sic")
            time.sleep(2)
            if subprocess.check_output(['paru', '-V']):
                print("Paru was installed successfully")
                return True
            else:
                return "Paru was not installed correctly"
        except:
            raise Exception("Problema con tu primo el paru")
            return False
    else:
        print("Git isn't installed, it will be installed")
        try:
            if install_pkg('git'):
                install_paru()
        except:
            raise Exception("There was a problem installing git")
            return False
        return False


def set_tor():
    time.sleep(1)
    try:
        subprocess.run(['paru', '-S', 'proxychains', 'tor', 'torsocks', '--noconfirm', '--needed'])
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


def install_packages():
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'tor'])
    except subprocess.CalledProcessError:
        print("Tor isn't running")
        return 1
    if check_process_status('tor'):
        try:
            subprocess.run(["proxychains4", "paru", "-S", "--noconfirm", ] \
                           + packages, check=True)
            return True
        except subprocess.CalledProcessError:
            print("There was an error downloading packages")
            return False
    else:
        raise Exception("There is a problem with tor process")
        return False


def main():
    print("Let's go")
    # init()
    time.sleep(1)
    print("Preparing folders...")
    time.sleep(2)
    if not os.path.exists('/usr/share/cybersec'):
        print("Cybersec path doesn't exists, creating it...")
        time.sleep(2)
        try:
            subprocess.run(['sudo', 'mkdir', '/usr/share/cybersec'], check=True)
            subprocess.run(['sudo', 'chown', f"{cur_user_uid}:{cur_user_gid}", '/usr/share/cybersec'], check=True)
            return True
        except subprocess.CalledProcessError:
            raise Exception(f"There was an error executing sudo")
            return False
    else:
        print("Cybersec path already exists continuing")
        time.sleep(2)
        pass
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
    if install_paru():
        set_tor()
        time.sleep(2)
        try:
            install_packages()
            print("Se instalo to...")
            pass
        except:
            time.sleep(2)
            raise Exception("Problemas descargando los paquetes.")
            return False
        time.sleep(2)
    else:
        print("There is an error on function install_paru()")
        return 1
    time.sleep(2)
    print("Setting configuration files...")
    os.system(f"cp -rf {install_dir}/zsh_powerlevel/p10k.zsh {home_path}/.p10k.zsh;"
              f"cp -rf {install_dir}/zsh_powerlevel/zshrc {home_path}/.zshrc;"
              f"cp -rf {install_dir}/config/alacritty.toml {home_path}/.alacritty.toml;"
              f"cp -rf {install_dir}/config/tmux.conf {home_path}/.tmux.conf;"
              f"cp -rf {install_dir}/config/nvim {config_dir}")
    os.system(f"cp -fr fonts {config_dir} && cd {config_dir}/fonts/Hack\
    && unzip Hack.zip && fc-cache -fv")
    os.system(f"git clone --depth=1 https://github.com/romkatv/powerlevel10k.git {home_path}/\
        powerlevel10k")
    time.sleep(2)
    return "FINISHED maybe..."


def sweet_script_o_mine():
    print(f"Starting\
    Checking configs for {cur_user} user:\
        Install directory: {install_dir}\
        Home directory: {home_path}\
        Config user directory: {config_dir}")
    time.sleep(3)
    print(f"The program needs that everything is updated, "
          f"do you want me to do it?")
    x = input("(y/n): ").lower()
    if x == 'y':
        try:
            if init():
                main()
        except Exception as e:
            stop_on_error(e)
    elif x == 'n':
        try:
            main()
        except:
            raise Exception("Something went wrong")
    else:
        print("Are you blind? Just type y or n")


# Checking if the process is being executed after a reboot
if subprocess.run(['crontab', '-l'], check=True):
    subprocess.run(['crontab', '-r'])
    main()
else:
    # Start the complete process #
    print("**** OH...SWEET SCRIPT O' MINE!! ****")
    time.sleep(2)
    if cur_user == 'root':
        raise Exception("This script can't be run as root")
    else:
        try:
            sweet_script_o_mine()
        except Exception as e:
            print("There was an error executing the sweet script")
            exit(51)
