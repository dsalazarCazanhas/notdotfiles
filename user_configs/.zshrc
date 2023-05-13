if [ $(whoami) = root ]; then
  export hello_root="BE CAREFUL!!! you are $(whoami)"
  echo $hello_root | cowsay | lolcat
else
  neofetch | lolcat
  export hello_user="HELLO!! $(whoami), today is $(date)"
  echo $hello_user | cowsay | lolcat
fi

if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi
typeset -g POWERLEVEL9K_INSTANT_PROMPT=quiet

#########################################################################################

export ZSH=/usr/share/oh-my-zsh/

ZSH_THEME="powerline"

# Plugins:
source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme

DISABLE_AUTO_TITLE="true"

COMPLETION_WAITING_DOTS="true"

# HIST_STAMPS="mm/dd/yyyy"

# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
plugins=(git zsh-syntax-highlighting zsh-autosuggestions history-substring-search docker sudo)

if [ -f $ZSH/oh-my-zsh.sh ]; then
  source $ZSH/oh-my-zsh.sh
fi

####   SETTINGS   ####
export PAGER='most'

setopt GLOB_DOTS
unsetopt SHARE_HISTORY

[[ $- != *i* ]] && return

export HISTCONTROL=ignoreboth:erasedups

# Make neovim the default editor
export EDITOR='lvim'
export VISUAL='bat'


if [ -d "$HOME/.bin" ] ;
  then PATH="$HOME/.bin:$PATH"
fi

if [ -d "$HOME/.local/bin" ] ;
  then PATH="$HOME/.local/bin:$PATH"
fi

### ALIASES ###

alias myProject='cd /home/dsalazar/Public/ProxYme'

#list
alias ls='lsd --color=auto'
alias la='lsd -a --group-directories-first'
alias ll='lsd -alFh --group-directories-first'
alias l='lsd'
#alias l.="lsd -A | egrep '^\.'"

#editing
alias rd=$VISUAL
alias wt=$EDITOR

#pacman easy
alias pacman='sudo pacman -S'
alias fullup='sudo pacman -Syyu'

#network
alias ports='ss -tulw'

#images
alias show='kitty +kitten icat'

#fix obvious typo's
alias cd..='cd ..'

## Colorize the grep command output for ease of use (good for log files)##
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'

#readable output
alias df='df -h'

#keyboard
alias give-me-azerty-be="sudo localectl set-x11-keymap be"
alias give-me-qwerty-us="sudo localectl set-x11-keymap us"

#setlocale
alias setlocale="sudo localectl set-locale LANG=en_US.UTF-8"
alias setlocales="sudo localectl set-x11-keymap be && sudo localectl set-locale LANG=en_US.UTF-8"

#pacman unlock
alias unlock="sudo rm /var/lib/pacman/db.lck"
alias rmpacmanlock="sudo rm /var/lib/pacman/db.lck"

#continue download
alias wget="wget -c"

#userlist
alias userlist="cut -d: -f1 /etc/passwd | sort"

#ps
alias psa="ps auxf"
alias psgrep="ps aux | grep -v grep | grep -i -e VSZ -e"

#grub update
alias update-grub="sudo grub-mkconfig -o /boot/grub/grub.cfg"

#add new fonts
alias update-fc='sudo fc-cache -fv'

#hardware info --short
alias hw="hwinfo --short"

#check vulnerabilities microcode
alias microcode='grep . /sys/devices/system/cpu/vulnerabilities/*'

#mounting the folder Public for exchange between host and guest on virtualbox
alias vbm="sudo /usr/local/bin/arcolinux-vbox-share"

alias cleanup='sudo pacman -Rns $(pacman -Qtdq)'

#clear
alias clean="clear; seq 1 $(tput cols) | sort -R | sparklines | lolcat"

#search content with ripgrep
alias rg="rg --sort path"

#get the error messages from journalctl
alias jctl="journalctl -p 3 -xb"

#nano for important configuration files
#know what you do in these files
alias nlxdm="sudo $EDITOR /etc/lxdm/lxdm.conf"
alias nlightdm="sudo $EDITOR /etc/lightdm/lightdm.conf"
alias npacman="sudo $EDITOR /etc/pacman.conf"
alias ngrub="sudo $EDITOR /etc/default/grub"
alias nconfgrub="sudo $EDITOR /boot/grub/grub.cfg"
alias nmkinitcpio="sudo $EDITOR /etc/mkinitcpio.conf"
alias nmirrorlist="sudo $EDITOR /etc/pacman.d/mirrorlist"
alias narcomirrorlist="sudo $EDITOR /etc/pacman.d/arcolinux-mirrorlist"
alias nsddm="sudo $EDITOR /etc/sddm.conf"
alias nsddmk="sudo $EDITOR /etc/sddm.conf.d/kde_settings.conf"
alias nfstab="sudo $EDITOR /etc/fstab"
alias nnsswitch="sudo $EDITOR /etc/nsswitch.conf"
alias nsamba="sudo $EDITOR /etc/samba/smb.conf"
alias ngnupgconf="sudo $EDITOR /etc/pacman.d/gnupg/gpg.conf"
alias nhosts="sudo $EDITOR /etc/hosts"
alias nhostname="sudo $EDITOR /etc/hostname"
alias nb="$EDITOR ~/.bashrc"
alias nz="$EDITOR ~/.zshrc"
alias nf="$EDITOR ~/.config/fish/config.fish"
alias nneofetch="$EDITOR ~/.config/neofetch/config.conf"

#reading logs with bat
alias lcalamares="bat /var/log/Calamares.log"
alias lpacman="bat /var/log/pacman.log"
alias lxorg="bat /var/log/Xorg.0.log"
alias lxorgo="bat /var/log/Xorg.0.log.old"

#gpg
#verify signature for isos
alias gpg-check="gpg2 --keyserver-options auto-key-retrieve --verify"
alias fix-gpg-check="gpg2 --keyserver-options auto-key-retrieve --verify"
#receive the key of a developer
alias gpg-retrieve="gpg2 --keyserver-options auto-key-retrieve --receive-keys"
alias fix-gpg-retrieve="gpg2 --keyserver-options auto-key-retrieve --receive-keys"
alias fix-keyserver="[ -d ~/.gnupg ] || mkdir ~/.gnupg ; cp /etc/pacman.d/gnupg/gpg.conf ~/.gnupg/ ; echo 'done'"

#systeminfo
alias probe="sudo -E hw-probe -all -upload"
alias sysfailed="systemctl list-units --failed"

#shutdown or reboot
alias shutdown="sudo shutdown now"
alias reboot="sudo reboot now"

#give the list of all installed desktops - xsessions desktops
alias xd="ls /usr/share/xsessions"
alias xdw="ls /usr/share/wayland-sessions"

#my functions
rmk () {
	scrub -p dod $1
	shred -zun 10 -v $1
}

# # ex = EXtractor for all kinds of archives
# # usage: ex <file>
ex ()
{
  if [ -f $1 ] ; then
    case $1 in
      *.tar.bz2)   tar xjf $1   ;;
      *.tar.gz)    tar xzf $1   ;;
      *.bz2)       bunzip2 $1   ;;
      *.rar)       unrar x $1   ;;
      *.gz)        gunzip $1    ;;
      *.tar)       tar xf $1    ;;
      *.tbz2)      tar xjf $1   ;;
      *.tgz)       tar xzf $1   ;;
      *.zip)       unzip $1     ;;
      *.Z)         uncompress $1;;
      *.7z)        7z x $1      ;;
      *.deb)       ar x $1      ;;
      *.tar.xz)    tar xf $1    ;;
      *.tar.zst)   tar xf $1    ;;
      *)           echo "'$1' cannot be extracted via ex()" ;;
    esac
  else
    echo "'$1' is not a valid file"
  fi
}

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
