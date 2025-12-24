#!/bin/bash
semanage login -a -s user_u "$1" 2>/dev/null || semanage login -m -s user_u "$1"
