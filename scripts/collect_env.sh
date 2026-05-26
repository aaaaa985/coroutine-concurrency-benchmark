#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

mkdir -p docs

{
  echo "===== OS ====="
  uname -a

  echo
  echo "===== Ubuntu ====="
  cat /etc/os-release

  echo
  echo "===== CPU ====="
  lscpu

  echo
  echo "===== Memory ====="
  free -h

  echo
  echo "===== Python ====="
  python3 --version

  echo
  echo "===== Java ====="
  java -version

  echo
  echo "===== Javac ====="
  javac -version

  echo
  echo "===== WSL ====="
  cat /proc/version
} &> docs/env.txt