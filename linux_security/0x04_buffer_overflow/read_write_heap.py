#!/usr/bin/python3

"""
read_write_heap.py

This script finds and replaces a string in the heap of a running process.

Usage:
    ./read_write_heap.py pid search_string replace_string

Arguments:
    pid             : The process ID of the running process.
    search_string   : The string to search for in the heap memory.
    replace_string  : The string to replace the search_string with.

The script reads the heap memory of the process with the given PID,
searches for the specified string, and replaces it if found. It
outputs a message indicating the result of the replacement.
"""

import sys
import os

def usage():
    """
    Prints the usage message and exits the program with status code 1.
    """
    print("Usage: read_write_heap.py pid search_string replace_string")
    sys.exit(1)

def main():
    """
    Main function to handle command-line arguments, locate the heap memory
    of the specified process, and replace occurrences of the search string
    with the replace string.

    Exits the program with status code 0 on successful replacement or status
    code 1 if the search string is not found or if an error occurs.
    """
    if len(sys.argv) != 4:
        usage()

    pid = int(sys.argv[1])
    search_string = sys.argv[2].encode()
    replace_string = sys.argv[3].encode()

    # Paths to the process's memory and mappings
    mem_path = f"/proc/{pid}/mem"
    maps_path = f"/proc/{pid}/maps"

    try:
        # Open the maps file to find heap memory regions
        with open(maps_path, 'r') as maps_file:
            for line in maps_file:
                parts = line.split()
                start = int(parts[0].split('-')[0], 16)
                end = int(parts[0].split('-')[1], 16)
                permissions = parts[1]

                # Check for heap memory regions with read-write permissions
                if 'heap' in line and 'rw-p' in permissions:
                    # Open the memory file for reading and writing
                    with open(mem_path, 'r+b') as mem_file:
                        mem_file.seek(start)
                        data = mem_file.read(end - start)

                        # Search for the string and replace it if found
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
