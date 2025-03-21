#!/bin/bash

function program_starter() {
  local address="$1"
  (echo -n "0x01 $address") | nc localhost 9999
}

function main() {
  program_starter "$1"
}

main "$@"
