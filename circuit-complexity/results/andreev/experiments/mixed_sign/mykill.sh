#!/bin/bash
# kill only my own python3/timeout processes whose command line contains the given pattern
pat="$1"
for pid in $(pgrep -u "$(id -u)" -f -- "$pat"); do
  [ "$pid" = "$$" ] && continue
  exe=$(tr '\0' ' ' < /proc/$pid/cmdline 2>/dev/null)
  case "$exe" in
    python3\ -I\ *|timeout\ *) echo "kill $pid: $exe"; kill "$pid";;
  esac
done
