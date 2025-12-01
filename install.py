# Install.py

import subprocess
import os
import time

packages = ['zip', 'unzip', 'alacritty',
            'dbus-glib', 'byobu', 'zsh',
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


def install_pkg(pkg: str) -> bool:
    try:
        subprocess.run(['sudo', 'pacman', '-S', pkg, '--noconfirm', '--needed'])
        return True
    except Exception:
        raise Exception(f"There was a problem installing {pkg}")


def install_oh_my_zsh():
    time.sleep(1)
    try:
        subprocess.run(["wget", "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"])
        subprocess.run(["sh", "install.sh", "--unattended"])
        time.sleep(3)
        return True
    except Exception as e:
        raise Exception(f"Problem installing oh-my-zsh: {e}")


def install_powerlevel10k():
    time.sleep(1)
    try:
        subprocess.run(["git", "clone" ,"--depth", "1", "https://github.com/romkatv/powerlevel10k.git", "~/.powerlevel10k"])
        return True
    except Exception:
        raise Exception("There was a problem installing powerlevel")


def install_fzf():
    try:
        subprocess.run(["git", "clone", "--depth", "1", "https://github.com/junegunn/fzf.git", "~/.fzf"])
        return True
    except Exception:
        raise Exception("There was an error installing fzf")


def install_packages():
    time.sleep(2)
    try:
        subprocess.run(["paru", "-S", "--noconfirm", "--needed", *packages])
        return True
    except subprocess.CalledProcessError as exc:
        print(f"There was an error downloading packages: {exc}")
        raise exc
    except Exception:
        raise


def prepare():
    time.sleep(1)
    
    try:
        install_packages()
    except Exception:
        raise Exception("A problem downloading the packages has occured")
    
    print("Installing OHMZSH...")
    time.sleep(2)
    try:
        install_oh_my_zsh()
    except Exception:
        raise
    
    print("Installing FZF...")
    time.sleep(3)
    try:
        install_fzf()
    except Exception:
        raise Exception("There was a problem installing fzf")

    
    print("Installing PWRLVL10K...")
    time.sleep(3)
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
              f"cp -rf {install_dir}/config/nvim {config_dir};")
    os.system(f"cp -fr fonts {config_dir} && cd {config_dir}/fonts/Hack && unzip Hack.zip && fc-cache -fv")
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

        Packages to be installed: {packages}
    """)
    time.sleep(3)
    print("OK, let's install then the things that matters. \\o/ ...")
    time.sleep(1)
    try:
        prepare()
    except Exception:
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
        try:
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
    except KeyboardInterrupt:
        print("\nOK, that's fine, you can stop this at any time. The SUN will be PRAISED anyway \\o/.")
        exit(0)

