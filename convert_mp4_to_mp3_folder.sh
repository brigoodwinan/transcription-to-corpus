#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_folder> <destination_folder>"
    exit 1
fi

SOURCE_FOLDER=$1
DESTINATION_FOLDER=$2

# Create the destination folder if it doesn't exist
mkdir -p "$DESTINATION_FOLDER"

# Loop through all mp4 files in the source folder
for file in "$SOURCE_FOLDER"/*.mp4; do
    if [ -f "$file" ]; then
        # Extract the base name without the extension
        base_name=$(basename "$file" .mp4)
        # Define the output mp3 file path
        output_file="$DESTINATION_FOLDER/$base_name.mp3"
        # Convert mp4 to mp3 using ffmpeg
        ffmpeg -i "$file" -vn -acodec libmp3lame -q:a 2 "$output_file"
        echo "Converted: '$file' -> '$output_file'"
    fi
done

echo "All files have been converted successfully."
