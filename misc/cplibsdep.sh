#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <binary> <destination_directory>"
    exit 1
fi

binary="$1"
destination_directory="$2"

# Check if the binary exists
if [ ! -e "$binary" ]; then
    echo "Error: Binary '$binary' not found."
    exit 1
fi

# Check if the destination directory exists
if [ ! -d "$destination_directory" ]; then
    echo "Error: Destination directory '$destination_directory' not found."
    exit 1
fi

# Use ldd to list library dependencies and extract library paths
libraries=$(ldd "$binary" | grep -E -o '/[^ ]+')

# Copy each library to the destination directory
for library in $libraries; do
    cp -vv --parents "$library" "$destination_directory"
done

echo "Library dependencies of '$binary' copied to '$destination_directory'."
