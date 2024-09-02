#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <parent_folder>"
    exit 1
fi

PARENT_FOLDER=$1

# Loop through each item in the parent folder
for item in "$PARENT_FOLDER"/*; do
    if [ -d "$item" ]; then
        echo "Processing subfolder: $item"
        python ./transcribe_mp3s_folder.py "$item"
    fi
done

echo "All subfolders have been processed."