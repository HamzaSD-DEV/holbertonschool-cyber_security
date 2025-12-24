#!/bin/bash
(command -v sestatus >/dev/null 2>&1 && sestatus | grep -i '^SELinux status:') || { m=$(getenforce 2>/dev/null | tr 'A-Z' 'a-z'); [ -n "$m" ] && echo "SELinux status:                 $m" || echo "SELinux status:                 unknown"; }
