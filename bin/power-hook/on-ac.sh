#!/usr/bin/env bash

LOG="$HOME/.local/state/power-hooks.log"

{
  echo "[$(date '+%F %T')] AC conectado"

  powerprofilesctl set performance

  containers=$(docker ps -aq)

  if [ -n "$containers" ]; then
    docker start $containers
  fi
} >>"$LOG" 2>&1
