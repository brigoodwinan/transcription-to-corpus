#!/Users/briangoodwin/personal/code-openai-transcription/env/bin/python

import argparse
import os

from pydub import AudioSegment


def split_mp3(
    input_file: str, destination_folder: str, max_chunk_size_mb: float
) -> None:
    """
    Split an MP3 file into smaller chunks based on a maximum file size.

    This function takes an MP3 file and splits it into smaller chunks, each
    with a file size less than the specified maximum chunk size. A 5-second
    overlap is added between consecutive chunks to ensure continuity.

    Args:
        input_file (str): The file path to the MP3 file that will be split.
        destination_folder (str): The directory where the split MP3 chunks will be saved.
        max_chunk_size_mb (float): The maximum size of each chunk in megabytes.

    Returns:
        None
    """
    # Load the MP3 file

    audio = AudioSegment.from_mp3(input_file)

    # duration in milliseconds
    total_duration_ms = len(audio)

    # approximate number of chunks required based on the file size
    file_size_mb = 1.1 * os.path.getsize(input_file) / 1e6  # 1.1 is a safety factor
    num_chunks = int(file_size_mb / max_chunk_size_mb) + 1

    # duration of each chunk
    chunk_duration_ms = total_duration_ms / num_chunks

    # overlap duration in milliseconds (5 seconds)
    overlap_duration_ms = 5000

    # Ensure destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for i in range(num_chunks):
        # Calculate the start time of the current chunk
        start_time = i * chunk_duration_ms
        # Adjust the end time to include overlap, except for the last chunk
        end_time = (
            start_time
            + chunk_duration_ms
            + (overlap_duration_ms if i < num_chunks - 1 else 0)
        )
        # Ensure end_time does not exceed total_duration_ms
        end_time = min(end_time, total_duration_ms)

        # Extract the chunk
        chunk = audio[start_time:end_time]

        # Generate filename with sequential numbering
        filename = f"{i+1}.mp3"
        full_path = os.path.join(destination_folder, filename)

        # Export the chunk to a new MP3 file
        chunk.export(full_path, format="mp3")

        print(f"Exported {full_path}")


def process_folder(folder_path: str, max_chunk_size_mb: float) -> None:
    """
    Process a folder of MP3 files, splitting each into smaller chunks.

    This function iterates through all MP3 files in a specified folder,
    splitting each file into smaller chunks based on the maximum chunk
    size provided. The chunks are saved in subdirectories named after
    the original file.

    Args:
        folder_path (str): The path to the folder containing MP3 files.
        max_chunk_size_mb (float): The maximum size of each chunk in megabytes.

    Returns:
        None
    """
    # Loop through all mp3 files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".mp3"):
            input_file = os.path.join(folder_path, file_name)
            base_name = os.path.splitext(file_name)[0]
            destination_folder = os.path.join(folder_path, base_name)

            print(f"Processing {input_file}...")
            split_mp3(input_file, destination_folder, max_chunk_size_mb)
    print("All files have been processed.")


def main():
    """
    Parse command-line arguments and process the folder of MP3 files.

    This function sets up an argument parser to receive the folder path and
    maximum chunk size from the command line. It then calls
    `process_folder` to handle the splitting of MP3 files in the specified
    folder into smaller chunks.

    Returns:
        None
    """
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Process a folder of MP3 files, splitting each into chunks of less than 25MB with 5 seconds of overlap."
    )
    parser.add_argument(
        "folder_path", type=str, help="The path to the folder containing MP3 files."
    )
    parser.add_argument(
        "--max_chunk_size_mb",
        type=float,
        default=25.0,
        help="Maximum size of each chunk in MB (default: 25MB).",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Process the folder with the provided arguments
    process_folder(args.folder_path, args.max_chunk_size_mb)


if __name__ == "__main__":
    main()
