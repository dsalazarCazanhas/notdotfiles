import subprocess
import os
import time

packages = ['zip', 'unzip', 'alacritty', 'tmux', 'kitty', 'git', 'oh-my-zsh-git',
            'dbus-glib', 'nmap-git', 'wireshark-git', 'virtualbox-bin',
            'virtualbox-bin-guest-iso', 'virtualbox-host-modules-arch',
            'diffutils', 'util-linux', 'less', 'most', 'debugedit', 'fakeroot',
            'gzip', 'binutils', 'bat', 'devtools', 'lsd', 'cowsay', 'toilet']
install_dir = os.path.dirname(__file__)
home_path = os.getenv('HOME')
config_dir = f"{home_path}/.config"
cur_user = subprocess.check_output(['id', '-un']).decode('utf-8').strip()
cur_user_uid = int(subprocess.check_output(['id', '-u']))
cur_user_gid = int(subprocess.check_output(['id', '-g']))
current_os = subprocess.check_output(["sed", "-n", "-e", "2p", "/etc/os-release"]).decode('utf-8').strip()
cyber_path = f"{home_path}/.local/share/cybersec"
start_title = """
***************************************************************************
*                                                                         *
*    OOOOO   H   H   H   H   H   H      SSSSS  W   W  EEEEE  EEEEE  TTTTT *
*    O   O   H   H   H   H   H   H      S      W   W  E      E        T   *
*    O   O   HHHHH   HHHHH   HHHHH      SSSSS  W W W  EEEEE  EEEEE    T   *
*    O   O   H   H   H   H   H   H          S  W W W  E      E        T   *
*    OOOOO   H   H   H   H   H   H      SSSSS  W   W  EEEEE  EEEEE    T   *
*                                                                         *
*                                                                         *
*                                                    ""                   *
*    SSSSS  CCCCC  RRRRR  IIIII  PPPPP  TTTTT        "" OOOOO             *
*    S      C      R   R    I    P   P    T          "" O   O             *
*    SSSSS  C      RRRR     I    PPPPP    T             O   O             *
*        S  C      R   R    I    P        T             O   O             *
*    SSSSS  CCCCC  R    R IIIII  P        T             OOOOO             *
*                                                                         *
*                                                                         *
*                                                                         *
*    M   M  IIIII  N   N  EEEEE  EEEEE  EEEEE  EEEEE  ! ! !               *
*    MM MM    I    NN  N  E      E      E      E      ! ! !               *
*    M M M    I    N N N  EEEEE  EEEEE  EEEEE  EEEEE  ! ! !               *
*    M   M    I    N  NN  E      E      E      E      ! ! !               *
*    M   M  IIIII  N   N  EEEEE  EEEEE  EEEEE  EEEEE  0 0 0               *
*                                                                         *
***************************************************************************
"""


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


def init():
    time.sleep(2)
    print("Executing first system upgrade.")
    time.sleep(1)
    subprocess.run(["sudo", "pacman-key", "--init"])
    subprocess.run(["sudo", "pacman-key", "--populate"])
    try:
        subprocess.run(["sudo", "pacman", "-Syyu", "--noconfirm"], check=True)
        time.sleep(3)
        reboot()
    except Exception:
        raise Exception("There was a problem in the first system upgrade.")


def install_paru():
    time.sleep(2)
    print("Installing the beloved PARU...")
    time.sleep(1)
    if subprocess.check_output(['git', '-v']):
        if subprocess.check_output(['paru', '-V']):
            print("Paru is already installed.")
            time.sleep(2)
            return True
        print("Git is installed, cloning paru...")
        time.sleep(2)
        try:
            subprocess.run(["git", "-C", "/tmp/", "clone", "https://aur.archlinux.org/paru-bin"])
            subprocess.run(["makepkg", "-sicD", "/tmp/paru-bin"])
            time.sleep(2)
            if subprocess.check_output(['paru', '-V']):
                print("Paru was installed correctly.")
                time.sleep(2)
                return True
        except Exception:
            raise
    else:
        print("Git isn't installed, it will be installed")
        try:
            install_pkg('git')
            if install_paru():
                return True
        except Exception:
            raise


def set_tor():
    time.sleep(1)
    try:
        subprocess.run(['paru', '-S', 'proxychains', 'tor', 'torsocks', '--noconfirm', '--needed'])
        return True
    except Exception:
        raise Exception("There was a problem installing TOR")


def install_oh_my_zsh():
    time.sleep(1)
    try:
        os.system("sh -c '$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)'")
        return True
    except:
        return False


def install_fzf():
    try:
        subprocess.run(["git", "clone --depth 1", "https://github.com/junegunn/fzf.git", "~/.fzf", "&&", "~/.fzf/install"])
        return True
    except Exception:
        raise Exception("There was an error installing fzf")


def install_packages():
    print("Let's install the things.")
    time.sleep(2)
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'tor'])
    except subprocess.CalledProcessError:
        raise
    try:
        subprocess.check_output(["proxychains4", "paru", "-S", "--noconfirm", *packages])
        return True
    except subprocess.CalledProcessError as exc:
        print(f"There was an error downloading packages: {exc}")
        raise exc
    except Exception:
        raise


def prepare():
    time.sleep(1)
    print("Preparing folders...")
    time.sleep(1)
    if not os.path.exists(cyber_path):
        print("Creating a folder to store cybersec tools.")
        time.sleep(2)
        try:
            subprocess.run(["mkdir", "-p", f"{cyber_path}"], check=True)
        except subprocess.CalledProcessError:
            raise
        except Exception:
            raise
    else:
        print("Cybersec path already exists continuing")
        time.sleep(2)
        pass
    time.sleep(2)
    print("Installing ohmyzsh")
    try:
        install_oh_my_zsh()
    #print("Installing FZF")
    #install_fzf()
    #time.sleep(2)
    #print("Setting commix, cyberchef and tor-browser")
    #os.system(f"git clone https://github.com/commixproject/commix.git {cybersec_path}/commix")
    #print("Downloading cyberchef")
    #os.system(f"mkdir {cybersec_path}/cyberchef")
    #os.system(f"curl https://gchq.github.io/CyberChef/CyberChef_v10.8.2.zip -o {cybersec_path}/cyberchef/cyber.zip")
    #os.system(f"cd {cybersec_path}/cyberchef && unzip cyber.zip")
    try:
        install_paru()
        time.sleep(2)
    except Exception:
        raise
    try:
        set_tor()
        time.sleep(2)
    except Exception:
        raise
    try:
        install_packages()
    except Exception:
        raise Exception("Problemas descargando los paquetes.")
    except subprocess.CalledProcessError:
        raise
    print("Setting configuration files...")
    time.sleep(2)
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
    print(f"""
    Starting...
    Current system: {current_os}
    Checking configs for {cur_user}:
        Install directory: {install_dir}
        
        Home directory: {home_path}
        
        Config user directory: {config_dir}

        Packages to install: {packages}
    """)
    time.sleep(3)
    print("The script needs that everything is updated, "
          "do you want me to do it?(It'll need root privileges)")
    x = input("(y/n): ").lower()
    if x == 'y':
        try:
            if init():
                main()
        except Exception as e:
            stop_on_error(e)
    elif x == 'n':
        print("OK, let's install then the things that matters. \\o/ ...")
        time.sleep(1)
        prepare()
    else:
        print("Are you blind? Just type Y or N,\
              lets start over.")
        sweet_script_o_mine()


def main():
    time.sleep(1)
    print("Mmmm... Let me think.")
    time.sleep(2)
    print('.')
    time.sleep(1)
    print('.')
    time.sleep(1)
    print('.')
    time.sleep(1)
    #if 'arch' not in current_os.lower():
    #    raise Exception(f"Sorry -->{current_os}<-- is not supported \nOther Systems that's not Arch Linux are not supported.....Yet :/ ")
    if os.geteuid() == 0:
        raise Exception("This script can't be run as root")
    else:
        print("Checking if the process is being executed after a reboot")
        time.sleep(3)
        try:
            if str(subprocess.run(['crontab', '-l']))[0] == 'n':
                print("Reboot completed, resuming...")
                time.sleep(3)
                subprocess.run(['crontab', '-r'])
            else:
                # Start the complete process #
                time.sleep(2)
                print("Starting for the first time, lets go!!")
                time.sleep(3)
                print(start_title)
                time.sleep(2)
                try:
                    sweet_script_o_mine()
                except Exception:
                    raise
        except Exception:
            raise
        except KeyboardInterrupt:
            raise


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print("\nOK, that's fine, you can stop this at any time. The SUN will be PRAISED anyways \\o/.")


