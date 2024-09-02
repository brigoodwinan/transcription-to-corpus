#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_folder> <output_file>"
    exit 1
fi

SOURCE_FOLDER=$1
OUTPUT_FILE=$2

# Initialize the output file
> "$OUTPUT_FILE"

# Find all text files recursively, sort them alphanumerically, and concatenate them into the output file
find "$SOURCE_FOLDER" -type f -name "*.txt" | sort | while read -r file; do
    # Print the fully resolved file path as a separator
    echo -e "\n\n\n<$file>\n\n" >> "$OUTPUT_FILE"
    # Concatenate the file content
    cat "$file" >> "$OUTPUT_FILE"
done

echo "All text files have been concatenated into $OUTPUT_FILE in alphanumeric order."