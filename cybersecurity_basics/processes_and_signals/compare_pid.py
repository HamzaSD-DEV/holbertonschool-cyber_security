#!/usr/bin/env python3
import os
import sys
import subprocess

def compare_pid(script_path):
    with open(script_path, 'r') as f:
        lines = f.readlines()
    
    cmds = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and not stripped.startswith('!'):
            cmds.append(stripped)
    
    if not cmds:
        sys.exit(1)
    
    script_cmds = '; '.join(cmds)
    cmd = 'echo "$$" > /tmp/expected; ' + script_cmds
    
    proc = subprocess.Popen(['bash', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    
    try:
        with open('/tmp/expected', 'r') as f:
            expected = f.read().strip()
        
        actual = stdout.decode().strip()
        
        if expected == actual:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: compare_pid.py <script_path>")
        sys.exit(1)
    
    compare_pid(sys.argv[1])
