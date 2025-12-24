#!/bin/bash
(command -v aa-status >/dev/null 2>&1 && aa-status) || (command -v apparmor_status >/dev/null 2>&1 && apparmor_status) || echo "AppArmor status tool not found"
