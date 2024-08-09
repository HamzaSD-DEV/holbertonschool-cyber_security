#!/bin/bash
cat <<< "$2  $1" | sha256sum -c -
