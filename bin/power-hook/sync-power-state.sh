#!/usr/bin/env bash

set -u

HOOK_DIR="$HOME/.local/bin/power-hook"
AC_STATE="/sys/class/power_supply/ACAD/online"

if [[ ! -r "$AC_STATE" ]]; then
  echo "No se puede leer $AC_STATE" >&2
  exit 1
fi

if [[ "$(cat "$AC_STATE")" == "1" ]]; then
  exec "$HOOK_DIR/on-ac.sh"
else
  exec "$HOOK_DIR/on-battery.sh"
fi
