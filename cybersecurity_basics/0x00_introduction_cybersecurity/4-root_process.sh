#!/bin/bash
cat <<< "^" #ps aux | grep "^$1" | grep -v ' 0  0 '
