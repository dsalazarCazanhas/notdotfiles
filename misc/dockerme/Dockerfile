FROM archlinux:latest
LABEL author="dsalazarCazanhas"
LABEL description="An arch image with some python core pkgs for testing apps.py"

RUN pacman-key --init && pacman-key --populate

RUN pacman -Sy  archlinux-keyring python python-pipenv python-pip python-virtualenv python-wheel nano most less base-devel sudo --noconfirm --needed

RUN useradd -m -G wheel myself

RUN sed -i 's/^#\s*\(%wheel ALL=(ALL:ALL) ALL\)/\1/' /etc/sudoers

RUN echo "12345" | passwd myself

RUN sed -i 's/^\(NoProgressBar\)/#\1/' /etc/pacman.conf

CMD ["/bin/bash"]
