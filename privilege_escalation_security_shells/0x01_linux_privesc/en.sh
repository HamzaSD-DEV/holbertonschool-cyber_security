#!/bin/bash

gen_flag () {
    md5sum <<< $(openssl aes-256-cbc -pass pass:$1 -nosalt -pbkdf2 <<< $2) | head -c 32
}


export github_username="HamzaSD-DEV"
export FLAG_0=$(gen_flag E5F6B7C8D9A01234 $github_username)

# Create the flag file and set appropriate permissions
echo "Holberton{root_periodic_script_escalation $FLAG_0}" 