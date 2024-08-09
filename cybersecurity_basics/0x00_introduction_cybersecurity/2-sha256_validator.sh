#!/bin/bash
sha256sum "$1" | grep -q "$2" && return 0 || return 1
