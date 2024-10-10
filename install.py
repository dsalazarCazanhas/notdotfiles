# Install.py

import subprocess
import os
import time

packages = ['zip', 'unzip', 'alacritty', 'tmux', 'kitty', 'git', 'oh-my-zsh-git',
            'dbus-glib', 'nmap-git', 'wireshark-git', 'virtualbox-bin', 'byobu',
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
            except Exception:
                raise
    elif x == 'n':
        return True
    else:
        print("Plz type y or n.")
        reboot()


def install_pkg(pkg: str) -> bool:
    try:
        subprocess.run(['sudo', 'pacman', '-S', pkg, '--noconfirm', '--needed'])
        return True
    except Exception:
        raise Exception(f"There was a problem installing {pkg}")

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
        subprocess.run(["curl", "-fsSL", "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"])
        return True
    except Exception:
        return False

def install_powerlevel10k():
    time.sleep(1)
    try:
        subprocess.run(["git", "clone --depth=1", "https://github.com/romkatv/powerlevel10k.git", "~/.powerlevel10k"])
        return True
    except Exception:
        raise Exception("There was a problem installing powerlevel")

def install_fzf():
    try:
        # check if zsh is installed
        subprocess.run(["git", "clone --depth 1", "https://github.com/junegunn/fzf.git", "~/.fzf"])
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
        subprocess.check_output(["proxychains4", "paru", "-S", "--noconfirm", "--needed", *packages])
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
    print("Installing ohmyzsh")
    try:
        install_oh_my_zsh()
    except Exception:
        raise
    print("Installing FZF")
    try:
        install_paru()
        time.sleep(2)
    except Exception:
        raise
    print("Setting TOR")
    time.sleep(2)
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
    time.sleep(1)
    try:
        install_fzf()
    except Exception:
        raise Exception("There was a problem installing fzf")
    try:
        install_powerlevel10k()
    except Exception:
        raise
    time.sleep(2)
    os.system(f"cp -rf {install_dir}/zsh_powerlevel/p10k.zsh {home_path}/.p10k.zsh;"
              f"cp -rf {install_dir}/zsh_powerlevel/zshrc {home_path}/.zshrc;"
              f"cp -rf {install_dir}/config/kitty {config_dir};"
              f"cp -rf {install_dir}/config/alacritty.toml {home_path}/.alacritty.toml;"
              f"cp -rf {install_dir}/config/tmux.conf {home_path}/.tmux.conf;"
              f"cp -rf {install_dir}/config/nvim {config_dir}")
    os.system(f"cp -fr fonts {config_dir} && cd {config_dir}/fonts/Hack\
    && unzip Hack.zip && fc-cache -fv")
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
    x = input("(y/N): ").lower()
    if x == 'y':
        try:
            init()
        except Exception as e:
            stop_on_error(e)
    else:
        print("OK, let's install then the things that matters. \\o/ ...")
        time.sleep(1)
        prepare()


def crontab():
    print("Checking for crontab job...")
    try:
        subprocess.run(["crontab", "-V"])
        if str(subprocess.run(['crontab', '-l']))[0] == 'n':
            print("Reboot completed, resuming...")
            time.sleep(3)
            subprocess.run(['crontab', '-r'])
            prepare()
        else:
            return False
    except FileNotFoundError:
        return False
    except Exception:
        raise
    except KeyboardInterrupt:
        raise


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
    if 'arch' not in current_os.lower():
        raise Exception(f"Sorry -->{current_os}<-- is not supported \nOther Systems that's not Arch Linux are not supported.....Yet :/ ")
    if os.geteuid() == 0:
        raise Exception("This script can't be run as root")
    else:
        print("Checking if the process is being executed after a reboot")
        time.sleep(3)
        try:
            if crontab():
                pass
            else:
                time.sleep(2)
                print("Starting for the first time, lets go!!")
                time.sleep(2)
                print(start_title)
                time.sleep(3)
                sweet_script_o_mine()
        except Exception:
            raise
        except KeyboardInterrupt:
            raise


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit(157)
    except FileNotFoundError as fne:
        print(e)
        exit(1)
    except KeyboardInterrupt:
        print("\nOK, that's fine, you can stop this at any time. The SUN will be PRAISED anyway \\o/.")
        exit(0)

