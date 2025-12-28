# Install.py - Arch Linux Configuration Script

import subprocess
import os
import sys
import logging
import shutil
from pathlib import Path
from typing import List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Constants
PACKAGES = [
    'zip', 'unzip', 'alacritty', 'dbus-glib', 'byobu', 'zsh',
    'diffutils', 'util-linux', 'less', 'most', 'debugedit', 'fakeroot',
    'gzip', 'binutils', 'bat', 'devtools', 'lsd', 'cowsay', 'toilet'
]

# Paths
INSTALL_DIR = Path(__file__).parent.absolute()
HOME_PATH = Path.home()
CONFIG_DIR = HOME_PATH / '.config'
ZSH_DIR = HOME_PATH / '.oh-my-zsh'
FZF_DIR = HOME_PATH / '.fzf'
P10K_DIR = HOME_PATH / '.powerlevel10k'

# System info
CUR_USER = subprocess.check_output(['id', '-un'], text=True).strip()
CUR_USER_UID = int(subprocess.check_output(['id', '-u'], text=True).strip())
CUR_USER_GID = int(subprocess.check_output(['id', '-g'], text=True).strip())
START_TITLE = """
***************************************************************************
*                                                                         *
*    OOOOO   H   H   H   H   H   H      SSSSS  W   W  EEEEE  EEEEE  TTTTT *
*    O   O   H   H   H   H   H   H      S      W   W  E      E        T   *
*    O   O   HHHHH   HHHHH   HHHHH      SSSSS  W W W  EEEEE  EEEEE    T   *
*    O   O   H   H   H   H   H   H          S  W W W  E      E        T   *
*    OOOOO   H   H   H   H   H   H      SSSSS  W   W  EEEEE  EEEEE    T   *
*                                                                         *
*                                                    ""                   *
*    SSSSS  CCCCC  RRRRR  IIIII  PPPPP  TTTTT        "" OOOOO             *
*    S      C      R   R    I    P   P    T          "" O   O             *
*    SSSSS  C      RRRR     I    PPPPP    T             O   O             *
*        S  C      R   R    I    P        T             O   O             *
*    SSSSS  CCCCC  R    R IIIII  P        T             OOOOO             *
*                                                                         *
*    M   M  IIIII  N   N  EEEEE  EEEEE  EEEEE  EEEEE  ! ! !               *
*    MM MM    I    NN  N  E      E      E      E      ! ! !               *
*    M M M    I    N N N  EEEEE  EEEEE  EEEEE  EEEEE  ! ! !               *
*    M   M    I    N  NN  E      E      E      E      ! ! !               *
*    M   M  IIIII  N   N  EEEEE  EEEEE  EEEEE  EEEEE  0 0 0               *
*                                                                         *
***************************************************************************
"""


def check_os() -> bool:
    """Check if the current OS is Arch Linux."""
    try:
        with open('/etc/os-release', 'r') as f:
            content = f.read().lower()
            return 'arch' in content
    except FileNotFoundError:
        return False


def run_command(cmd: List[str], error_msg: str, check: bool = True) -> Tuple[bool, str]:
    """Execute a command and handle errors consistently."""
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"{error_msg}: {e.stderr}")
        return False, e.stderr
    except Exception as e:
        logger.error(f"{error_msg}: {str(e)}")
        return False, str(e)


def install_pkg(pkg: str) -> bool:
    """Install a single package using pacman."""
    logger.info(f"Installing {pkg}...")
    success, _ = run_command(
        ['sudo', 'pacman', '-S', pkg, '--noconfirm', '--needed'],
        f"Failed to install {pkg}"
    )
    return success


def install_oh_my_zsh() -> bool:
    """Install Oh My Zsh if not already installed."""
    if ZSH_DIR.exists():
        logger.info("Oh My Zsh already installed, skipping...")
        return True
    
    logger.info("Installing Oh My Zsh...")
    install_script = HOME_PATH / 'install.sh'
    
    try:
        # Download install script
        success, _ = run_command(
            ['wget', 'https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh',
             '-O', str(install_script)],
            "Failed to download Oh My Zsh installer"
        )
        if not success:
            return False
        
        # Run installer
        success, _ = run_command(
            ['sh', str(install_script), '--unattended'],
            "Failed to install Oh My Zsh"
        )
        
        # Cleanup
        if install_script.exists():
            install_script.unlink()
        
        return success
    except Exception as e:
        logger.error(f"Error installing Oh My Zsh: {e}")
        return False


def install_powerlevel10k() -> bool:
    """Install Powerlevel10k theme if not already installed."""
    if P10K_DIR.exists():
        logger.info("Powerlevel10k already installed, skipping...")
        return True
    
    logger.info("Installing Powerlevel10k...")
    success, _ = run_command(
        ['git', 'clone', '--depth', '1',
         'https://github.com/romkatv/powerlevel10k.git', str(P10K_DIR)],
        "Failed to install Powerlevel10k"
    )
    return success


def install_fzf() -> bool:
    """Install fzf if not already installed."""
    if FZF_DIR.exists():
        logger.info("fzf already installed, skipping...")
        return True
    
    logger.info("Installing fzf...")
    success, _ = run_command(
        ['git', 'clone', '--depth', '1',
         'https://github.com/junegunn/fzf.git', str(FZF_DIR)],
        "Failed to install fzf"
    )
    
    if success and FZF_DIR.exists():
        # Run fzf installer
        install_script = FZF_DIR / 'install'
        if install_script.exists():
            run_command(
                [str(install_script), '--all'],
                "Failed to run fzf installer",
                check=False
            )
    
    return success


def install_packages() -> bool:
    """Install all required packages using paru."""
    logger.info("Installing required packages...")
    
    # Check if paru is available
    if shutil.which('paru') is None:
        logger.warning("paru not found, trying with pacman...")
        cmd = ['sudo', 'pacman', '-S', '--noconfirm', '--needed'] + PACKAGES
    else:
        cmd = ['paru', '-S', '--noconfirm', '--needed'] + PACKAGES
    
    success, _ = run_command(cmd, "Failed to install packages")
    return success


def copy_config_files() -> bool:
    """Copy configuration files to their destination."""
    logger.info("Copying configuration files...")
    
    configs = [
        (INSTALL_DIR / 'zsh_powerlevel' / 'p10k.zsh', HOME_PATH / '.p10k.zsh'),
        (INSTALL_DIR / 'zsh_powerlevel' / 'zshrc', HOME_PATH / '.zshrc'),
        (INSTALL_DIR / 'config' / 'kitty', CONFIG_DIR / 'kitty'),
        (INSTALL_DIR / 'config' / 'alacritty.toml', HOME_PATH / '.alacritty.toml'),
        (INSTALL_DIR / 'config' / 'tmux.conf', HOME_PATH / '.tmux.conf'),
        (INSTALL_DIR / 'config' / 'nvim', CONFIG_DIR / 'nvim'),
    ]
    
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        for src, dst in configs:
            if not src.exists():
                logger.warning(f"Source not found: {src}, skipping...")
                continue
            
            # Backup existing config if it exists
            if dst.exists():
                backup = Path(str(dst) + '.backup')
                logger.info(f"Backing up existing config: {dst} -> {backup}")
                if dst.is_dir():
                    shutil.copytree(dst, backup, dirs_exist_ok=True)
                else:
                    shutil.copy2(dst, backup)
            
            # Copy new config
            logger.info(f"Copying {src.name} -> {dst}")
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        
        return True
    except Exception as e:
        logger.error(f"Error copying config files: {e}")
        return False


def install_fonts() -> bool:
    """Install Hack fonts."""
    logger.info("Installing fonts...")
    
    fonts_src = INSTALL_DIR / 'fonts'
    fonts_dst = CONFIG_DIR / 'fonts'
    hack_dir = fonts_dst / 'Hack'
    
    try:
        if not fonts_src.exists():
            logger.warning("Fonts directory not found, skipping...")
            return True
        
        # Copy fonts directory
        shutil.copytree(fonts_src, fonts_dst, dirs_exist_ok=True)
        
        # Unzip Hack fonts if zip exists
        hack_zip = hack_dir / 'Hack.zip'
        if hack_zip.exists():
            logger.info("Extracting Hack fonts...")
            success, _ = run_command(
                ['unzip', '-o', str(hack_zip), '-d', str(hack_dir)],
                "Failed to extract Hack fonts",
                check=False
            )
            
            # Refresh font cache
            logger.info("Refreshing font cache...")
            run_command(['fc-cache', '-fv'], "Failed to refresh font cache", check=False)
        
        return True
    except Exception as e:
        logger.error(f"Error installing fonts: {e}")
        return False


def prepare() -> bool:
    """Main preparation and installation function."""
    steps = [
        ("Installing packages", install_packages),
        ("Installing Oh My Zsh", install_oh_my_zsh),
        ("Installing fzf", install_fzf),
        ("Installing Powerlevel10k", install_powerlevel10k),
        ("Copying configuration files", copy_config_files),
        ("Installing fonts", install_fonts),
    ]
    
    for step_name, step_func in steps:
        logger.info(f"\n{'='*60}")
        logger.info(f"Step: {step_name}")
        logger.info(f"{'='*60}")
        
        if not step_func():
            logger.error(f"Failed: {step_name}")
            return False
    
    return True


def display_system_info():
    """Display system and configuration information."""
    try:
        with open('/etc/os-release', 'r') as f:
            os_info = [line.strip() for line in f.readlines() if 'PRETTY_NAME' in line][0]
            os_info = os_info.split('=')[1].strip('"')
    except Exception:
        os_info = "Unknown"
    
    info = f"""
    {'='*70}
    Starting Configuration Script
    {'='*70}
    Current System: {os_info}
    Current User: {CUR_USER} (UID: {CUR_USER_UID}, GID: {CUR_USER_GID})
    Install Directory: {INSTALL_DIR}
    Home Directory: {HOME_PATH}
    Config Directory: {CONFIG_DIR}
    Packages to Install: {len(PACKAGES)} packages
    {'='*70}
    """
    logger.info(info)


def main():
    """Main execution function."""
    # Check if running as root
    if os.geteuid() == 0:
        logger.error("This script cannot be run as root!")
        sys.exit(1)
    
    # Check if running on Arch Linux
    if not check_os():
        logger.error("This script only supports Arch Linux!")
        sys.exit(1)
    
    # Display banner and system info
    print(START_TITLE)
    display_system_info()
    
    # Confirm before proceeding
    try:
        response = input("\n¿Continuar con la instalación? (y/N): ").strip().lower()
        if response not in ['y', 'yes', 's', 'si', 'sí']:
            logger.info("Installation cancelled by user.")
            sys.exit(0)
    except KeyboardInterrupt:
        logger.info("\nInstallation cancelled by user.")
        sys.exit(0)
    
    # Run preparation and installation
    logger.info("\n🚀 Starting installation process...\n")
    
    if prepare():
        logger.info("\n" + "="*70)
        logger.info("✅ Installation completed successfully!")
        logger.info("="*70)
        logger.info("\nNext steps:")
        logger.info("  1. Restart your terminal or run: source ~/.zshrc")
        logger.info("  2. Configure Powerlevel10k: p10k configure")
        logger.info("  3. Enjoy your new setup! \\o/")
        sys.exit(0)
    else:
        logger.error("\n" + "="*70)
        logger.error("❌ Installation failed!")
        logger.error("="*70)
        logger.error("Check the logs above for details.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\n✋ Installation interrupted by user.")
        logger.info("The SUN will be PRAISED anyway \\o/")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

