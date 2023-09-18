#!/bin/sh

revert() {
  rm /tmp/*screen*.png
  xset dpms 0 0 0
}
trap revert HUP INT TERM
xset +dpms dpms 0 30 5
scrot -d 1 /tmp/locking_screen.png
convert -blur 0x8 /tmp/locking_screen.png /tmp/screen_blur.png
convert -composite /tmp/screen_blur.png ~/.config/i3lock/rick.png -geometry -20x1200 /tmp/screen.png
convert -composite /tmp/screen.png ~/.config/i3lock/glados_edited.png -geometry +550 /tmp/screen.png
i3lock -i /tmp/screen.png -te
revert
