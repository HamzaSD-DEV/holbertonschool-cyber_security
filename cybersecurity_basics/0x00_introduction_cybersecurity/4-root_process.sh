#!/bin/bash
cat <<< "^" #ps aux "^$1" grep -v
