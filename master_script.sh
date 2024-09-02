#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <source_mp4_folder> <destination_mp3_folder_and_parent_folder> <max_chunk_size_mb> <output_text_file>"
    exit 1
fi

# Assign command-line arguments to variables
SOURCE_MP4_FOLDER=$1
DESTINATION_MP3_FOLDER_AND_PARENT_FOLDER=$2
MAX_CHUNK_SIZE_MB=$3
OUTPUT_TEXT_FILE=$4

# Step 1: Convert MP4 files to MP3
echo "Converting MP4 files to MP3..."
bash ./convert_mp4_to_mp3_folder.sh "$SOURCE_MP4_FOLDER" "$DESTINATION_MP3_FOLDER_AND_PARENT_FOLDER"
if [ $? -ne 0 ]; then
    echo "Error during MP4 to MP3 conversion."
    exit 1
fi
echo "MP4 to MP3 conversion completed."

# Step 2: Split MP3 files into smaller chunks
echo "Splitting MP3 files into smaller chunks..."
python ./mp3_into_25mb_chunks_folder.py "$DESTINATION_MP3_FOLDER_AND_PARENT_FOLDER" --max_chunk_size_mb "$MAX_CHUNK_SIZE_MB"
if [ $? -ne 0 ]; then
    echo "Error during MP3 chunking."
    exit 1
fi
echo "MP3 chunking completed."

# Step 3: Process subfolders of MP3 chunks for transcription
echo "Processing subfolders for transcription..."
bash ./process_subfolders_of_mp3s.sh "$DESTINATION_MP3_FOLDER_AND_PARENT_FOLDER"
if [ $? -ne 0 ]; then
    echo "Error during subfolder processing."
    exit 1
fi
echo "Subfolder processing completed."

# Step 4: Concatenate all text files into a single output file
echo "Concatenating text files into a single output file..."
bash ./concatenate_text_files.sh "$DESTINATION_MP3_FOLDER_AND_PARENT_FOLDER" "$OUTPUT_TEXT_FILE"
if [ $? -ne 0 ]; then
    echo "Error during text file concatenation."
    exit 1
fi
echo "Text file concatenation completed."

echo "All steps completed successfully."