#!/bin/bash
if command -v sestatus >/dev/null 2>&1; then
  sestatus | grep -i "^SELinux status:"
elif command -v getenforce >/dev/null 2>&1; then
  mode=$(getenforce | tr 'A-Z' 'a-z')
  echo "SELinux status:                 $mode"
else
  echo "SELinux status:                 unknown"
fi
