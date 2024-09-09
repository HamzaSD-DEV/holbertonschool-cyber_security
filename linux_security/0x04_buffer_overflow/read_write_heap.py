#!/usr/bin/python3

"""
This script finds and replaces a string in the heap of a running process.
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
    Main function to handle command-line arguments.
    """
    if len(sys.argv) != 4:
        usage()

    pid = int(sys.argv[1])
    search_string = sys.argv[2].encode()
    replace_string = sys.argv[3].encode()

    mem_path = f"/proc/{pid}/mem"
    maps_path = f"/proc/{pid}/maps"

    try:
        """
        Open the maps file to find heap memory regions
        """
        with open(maps_path, 'r') as maps_file:
            for line in maps_file:
                parts = line.split()
                start = int(parts[0].split('-')[0], 16)
                end = int(parts[0].split('-')[1], 16)
                permissions = parts[1]
                """
                Check for heap memory regions with read-write permissions
                """
                if 'heap' in line and 'rw-p' in permissions:
                    """
                    Open the memory file for reading and writing
                    """
                    with open(mem_path, 'r+b') as mem_file:
                        mem_file.seek(start)
                        data = mem_file.read(end - start)
                        """
                        Search for the string and replace it if found
                        """
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
"""
end of program
"""
if __name__ == "__main__":
    main()
"""
end of document
"""