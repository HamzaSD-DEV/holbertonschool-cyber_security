#!/bin/bash

gen_flag () {
    md5sum <<< $(openssl aes-256-cbc -pass pass:$1 -nosalt -pbkdf2 <<< $2) | head -c 32
}

gen_flag2 () {
    md5sum <<< $(openssl aes-256-cbc -pass pass:EBXT7S8D69GUACKK -nosalt -pbkdf2 <<< HamzaSD-DEV) | head -c 32
}
gen_flag2


export github_username="HamzaSD-DEV"
export FLAG_0=$(gen_flag EBXT7S8D69GUACKK $github_username)

# Create the flag file and set appropriate permissions
echo "Holberton{root_periodic_script_escalation $FLAG_0}" 