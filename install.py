# Install.py - Arch Linux Configuration Script

import logging
import os
import pwd
import shutil
import subprocess
import sys
from pathlib import Path

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
    'gzip', 'binutils', 'bat', 'devtools', 'lsd', 'cowsay', 'toilet',
    'git', 'lolcat', 'ttf-hack-nerd', 'neovim', 'ripgrep', 'fd', 'lazygit',
    'scrub', 'hw-probe'
]

# Paths
INSTALL_DIR = Path(__file__).parent.absolute()
HOME_PATH = Path.home()
CONFIG_DIR = HOME_PATH / '.config'
ZSH_DIR = HOME_PATH / '.oh-my-zsh'
FZF_DIR = HOME_PATH / '.fzf'
P10K_DIR = HOME_PATH / '.powerlevel10k'
NVIM_DIR = CONFIG_DIR / 'nvim'
ALACRITTY_THEMES_DIR = CONFIG_DIR / 'alacritty' / 'themes'
ZSH_PLUGINS_DIR = ZSH_DIR / 'custom' / 'plugins'
ZSH_PLUGINS = {
    'zsh-autosuggestions': 'https://github.com/zsh-users/zsh-autosuggestions.git',
    'zsh-syntax-highlighting': 'https://github.com/zsh-users/zsh-syntax-highlighting.git',
}

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


def run_command(
    cmd: list[str], error_msg: str, check: bool = True, cwd: Path | None = None
) -> tuple[bool, str]:
    """Execute a command and handle errors consistently."""
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"{error_msg}: {e.stderr}")
        return False, e.stderr
    except OSError as e:
        logger.error(f"{error_msg}: {e}")
        return False, str(e)


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
            ['curl', '-fsSL', 'https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh',
             '-o', str(install_script)],
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
    except OSError as e:
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


def install_zsh_plugins() -> bool:
    """Clone the Oh My Zsh custom plugins used by the zshrc plugins list."""
    for name, url in ZSH_PLUGINS.items():
        plugin_dir = ZSH_PLUGINS_DIR / name
        if plugin_dir.exists():
            logger.info(f"{name} already installed, skipping...")
            continue

        logger.info(f"Installing {name}...")
        success, _ = run_command(
            ['git', 'clone', '--depth', '1', url, str(plugin_dir)],
            f"Failed to install {name}"
        )
        if not success:
            return False

    return True


def install_lazyvim() -> bool:
    """Install LazyVim starter config if not already installed."""
    if NVIM_DIR.exists():
        logger.info("Neovim config already present, skipping LazyVim...")
        return True

    logger.info("Installing LazyVim starter...")
    success, _ = run_command(
        ['git', 'clone', 'https://github.com/LazyVim/starter', str(NVIM_DIR)],
        "Failed to clone LazyVim starter"
    )
    if success:
        shutil.rmtree(NVIM_DIR / '.git', ignore_errors=True)
    return success


def install_alacritty_theme() -> bool:
    """Install the alacritty-theme collection if not already installed."""
    if ALACRITTY_THEMES_DIR.exists():
        logger.info("alacritty-theme already installed, skipping...")
        return True

    logger.info("Installing alacritty-theme...")
    ALACRITTY_THEMES_DIR.parent.mkdir(parents=True, exist_ok=True)
    success, _ = run_command(
        ['git', 'clone', '--depth', '1',
         'https://github.com/alacritty/alacritty-theme.git', str(ALACRITTY_THEMES_DIR)],
        "Failed to install alacritty-theme"
    )
    return success


def install_yay() -> bool:
    """Build and install the yay AUR helper if it isn't already present.

    Needed on vanilla Arch (unlike EndeavourOS, it doesn't ship with an AUR
    helper), since install_packages() relies on yay to pull AUR-only
    packages like scrub and hw-probe.
    """
    if shutil.which('yay') is not None:
        logger.info("yay already installed, skipping...")
        return True

    logger.info("Installing yay (AUR helper)...")
    success, _ = run_command(
        ['sudo', 'pacman', '-S', '--noconfirm', '--needed', 'base-devel', 'git'],
        "Failed to install base-devel/git"
    )
    if not success:
        return False

    build_dir = HOME_PATH / '.cache' / 'yay-bin-install'
    shutil.rmtree(build_dir, ignore_errors=True)

    success, _ = run_command(
        ['git', 'clone', '--depth', '1', 'https://aur.archlinux.org/yay-bin.git', str(build_dir)],
        "Failed to clone yay-bin from the AUR"
    )
    if not success:
        return False

    success, _ = run_command(
        ['makepkg', '-si', '--noconfirm'],
        "Failed to build yay-bin",
        cwd=build_dir
    )
    shutil.rmtree(build_dir, ignore_errors=True)
    return success


def update_system() -> bool:
    """Sync repos and fully upgrade the system before installing anything new.

    Installing packages without a preceding full upgrade risks a partial
    upgrade, a common source of broken dependencies on Arch.
    """
    logger.info("Updating system...")
    if shutil.which('yay') is None:
        cmd = ['sudo', 'pacman', '-Syu', '--noconfirm']
    else:
        cmd = ['yay', '-Syu', '--noconfirm']

    success, _ = run_command(cmd, "Failed to update system")
    return success


def install_packages() -> bool:
    """Install all required packages using yay."""
    logger.info("Installing required packages...")

    # Check if yay is available
    if shutil.which('yay') is None:
        logger.warning("yay not found, trying with pacman...")
        cmd = ['sudo', 'pacman', '-S', '--noconfirm', '--needed'] + PACKAGES
    else:
        cmd = ['yay', '-S', '--noconfirm', '--needed'] + PACKAGES

    success, _ = run_command(cmd, "Failed to install packages")
    return success


def copy_config_files() -> bool:
    """Copy configuration files to their destination."""
    logger.info("Copying configuration files...")
    
    configs = [
        (INSTALL_DIR / 'zsh_powerlevel' / 'p10k.zsh', HOME_PATH / '.p10k.zsh'),
        (INSTALL_DIR / 'zsh_powerlevel' / 'zshrc', HOME_PATH / '.zshrc'),
        (INSTALL_DIR / 'dircolors', HOME_PATH / '.dircolors'),
        (INSTALL_DIR / 'config' / 'alacritty.toml', CONFIG_DIR / 'alacritty' / 'alacritty.toml'),
        (INSTALL_DIR / 'config' / 'byobu', CONFIG_DIR / 'byobu'),
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
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        
        return True
    except OSError as e:
        logger.error(f"Error copying config files: {e}")
        return False


def refresh_font_cache() -> bool:
    """Refresh the fontconfig cache after installing font packages."""
    logger.info("Refreshing font cache...")
    run_command(['fc-cache', '-fv'], "Failed to refresh font cache", check=False)
    return True


def set_default_shell() -> bool:
    """Set zsh as the user's default login shell.

    Oh My Zsh's --unattended install deliberately skips chsh, so this has
    to happen explicitly or the user stays on their old shell.
    """
    zsh_path = shutil.which('zsh')
    if zsh_path is None:
        logger.warning("zsh not found, skipping shell change...")
        return True

    if pwd.getpwnam(CUR_USER).pw_shell == zsh_path:
        logger.info("zsh is already the default shell, skipping...")
        return True

    logger.info("Setting zsh as the default shell...")
    success, _ = run_command(
        ['sudo', 'chsh', '-s', zsh_path, CUR_USER],
        "Failed to set default shell"
    )
    return success


def prepare() -> bool:
    """Main preparation and installation function."""
    steps = [
        ("Updating system", update_system),
        ("Installing yay", install_yay),
        ("Installing packages", install_packages),
        ("Installing Oh My Zsh", install_oh_my_zsh),
        ("Installing zsh plugins", install_zsh_plugins),
        ("Installing fzf", install_fzf),
        ("Installing Powerlevel10k", install_powerlevel10k),
        ("Installing LazyVim", install_lazyvim),
        ("Installing alacritty-theme", install_alacritty_theme),
        ("Copying configuration files", copy_config_files),
        ("Refreshing font cache", refresh_font_cache),
        ("Setting default shell", set_default_shell),
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
            os_info = next((line.strip() for line in f if 'PRETTY_NAME' in line), '')
            os_info = os_info.split('=')[1].strip('"')
    except (OSError, IndexError):
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
        response = input("\nContinue with installation? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
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
    except Exception as e:  # noqa: BLE001 - top-level safety net, must catch anything unexpected
        logger.error(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

