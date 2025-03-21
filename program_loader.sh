#!/bin/bash

function program_loader() {
  local filepath="$1"
  local address="$2"
  if [ -f "$filepath" ]; then
    (echo -n "0x00 $address " && cat $filepath) | nc localhost 9999
    return 0
  else
    echo "The file does not exist"
    return 1
  fi
}

function main() {
  program_loader "$1" "$2"
}

main "$@"
