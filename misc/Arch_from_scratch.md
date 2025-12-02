# MI OS Archlinux de cero.

## Instalacion en UEFI-MODE
**Para saber arquitectura y si esta en uefi**
`cat /sys/firmware/efi/fw_platform_size`
`Output: 64` – UEFIx64

**Particionar con cfdisk (gpt):**
1. part root `/`
2. part efi `/efi` 1gib
3. part swap min 4gib
Formatear las particiones creadas con `mkfs.fat -F 32 /dev/sdax`
La partición de datos con `mkfs.ext4 /dev/sdax`
Se asigna la partición swap con `mkswap /dev/sdax` que sería la partición swap y se activa con `swapon`. Alternativamente se puede evitar el swap en disco usando `swap on zram` luego de instalado el sistema.

**Verificar las particiones usando lsblk**
Montar las particiones pertinentes usando mount
La partición del sistema `mount /dev/sdax /mnt`; 
la carpeta boot: `mount -m /dev/efi_partition mnt/boot/efi`

**Lo siguiente es verificar que se tenga internet.**
Si es ethernet es asegurarse con ping a Google si tiene internet, en caso de WiFi usar la herramienta por defecto que trae arch con 
`iwctl station wlan0 connect SSID` y poner el password cuando lo pida. 

**Proceder a actualizar las db.**
```shell
pacman -Syy
pacman-key –init && pacman-key –populate
```

**Se procede a instalar el sistema...**
- `pacstrap /mnt linux linux-headers linux-firmware base base-devel grub networkmanager wpa_supplicant git efibootmgr vim nano wget man-db man-pages texinfo`
- *Al terminar la instalación se graba la tabla de particiones*
`genfstab -U /mnt >> /mnt/etc/fstab`
- *Se define el nombre del host*
`echo ‘el nombre del pc’ >> /mnt/etc/hostname`
- Se accede al entorno acabado de instalar como root usando `arch-chroot /mnt`
- Time zone: `ln -sf /usr/share/zoneinfo/Region/City /etc/localtime`
`hwclock --systohc` para crear */etc/adjtime*
- Editar */etc/locale.gen* y descomentar `en_US.UTF-8 UTF-8`, luego ejecutar `locale-gen`
- Crear */etc/locale.conf* y agregar `LANG=en_US.UTF-8`

Para listar los mapas de teclado disponibles `localectl list-keymaps` 
Para el teclado */etc/vconsole.conf*, `KEYMAP=en`


**Passwords**
Si queremos agregar usuario con privilegios de root `useradd -m( para crearle un home) ‘el nombre del usuario’ -G wheel`
activar el grupo wheel en */etc/sudoers*, buscar la línea donde esta `# %wheel` y quitarle el `#` para activar el grupo, los mas avanzados usaran sudoers.d.
Se le asigna el password al nuevo usuario 
`passwd ‘usuario’`

Se configura el arranque con:
- para UEFI `grub-install --target=x86_64-efi /dev/sdx`(donde este el dir efi) 
- se configuran las grub con `grub-mkconfig -o /boot/grub/grub.cfg`
*Salimos del entorno root con exit* Y reiniciamos para entrar al sistema operativo que acabamos de instalar. Recordar retirar la imagen de arranque de arch.
> [!NOTE]
> **PARU** `git clone https://aur.archlinux.org/paru-bin && cd paru-bin && makepkg -sic`
> **Activar NetworkManager luego de reiniciar** `sudo systemctl enable NetworkManager && sudo systemctl start NetworkManager`
