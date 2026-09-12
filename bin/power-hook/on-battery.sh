#!/usr/bin/env bash

LOG="$HOME/.local/state/power-hooks.log"

{
  echo "[$(date '+%F %T')] Entrando en batería"

  powerprofilesctl set power-saver

  containers=$(docker ps -q)

  if [ -n "$containers" ]; then
    docker stop $containers
  fi
} >>"$LOG" 2>&1
