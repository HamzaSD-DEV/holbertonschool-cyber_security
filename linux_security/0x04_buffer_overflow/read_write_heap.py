#!/usr/bin/python3
import sys
import os
"""
read_write_heap.py

A script to find and replace a string in the heap of a running process.

Usage:
    ./read_write_heap.py pid search_string replace_string

Arguments:
    pid             : The PID of the running process.
    search_string   : The string to search for in the heap.
    replace_string  : The string to replace the search_string with.
"""
def usage():
    """
    Print the usage message and exit with status code 1.
    """
    print("Usage: read_write_heap.py pid search_string replace_string")
    sys.exit(1)

def main():
    """
    Main function to handle the script execution.
    It reads the process memory and replaces the search_string with replace_string.
    """
    if len(sys.argv) != 4:
        usage()

    pid = int(sys.argv[1])
    search_string = sys.argv[2].encode()
    replace_string = sys.argv[3].encode()

    # Paths to the process's memory
    mem_path = f"/proc/{pid}/mem"
    maps_path = f"/proc/{pid}/maps"

    try:
        with open(maps_path, 'r') as maps_file:
            for line in maps_file:
                parts = line.split()
                start = int(parts[0].split('-')[0], 16)
                end = int(parts[0].split('-')[1], 16)
                permissions = parts[1]

                if 'heap' in line and 'rw-p' in permissions:
                    with open(mem_path, 'r+b') as mem_file:
                        mem_file.seek(start)
                        data = mem_file.read(end - start)

                        index = data.find(search_string)
                        if index != -1:
                            new_data = data[:index] + replace_string + data[index + len(search_string):]
                            mem_file.seek(start)
                            mem_file.write(new_data)
                            print(f"Replaced '{search_string.decode()}' with '{replace_string.decode()}'")
                            sys.exit(0)
        print("Error: String not found in heap")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
