#!/bin/bash
cat "$1" | sha256sum -c
