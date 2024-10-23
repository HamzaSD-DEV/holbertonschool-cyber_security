#!/bin/bash

gen_flag () {
    md5sum <<< $(openssl aes-256-cbc -pass pass:$1 -nosalt -pbkdf2 <<< HamzaSD-DEV) | head -c 32
}


gen_flag