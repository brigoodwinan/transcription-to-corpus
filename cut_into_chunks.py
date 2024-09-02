import argparse
import os

from pydub import AudioSegment


def split_mp3(input_file: str, destination_folder: str, num_chunks: int) -> None:
    """
    Split a large MP3 file into a specified number of equal-sized chunks with overlap.

    This function takes an MP3 file and splits it into the specified number of chunks.
    Each chunk is of equal duration, with a 5-second overlap between consecutive chunks.
    The resulting chunks are saved as new MP3 files in the specified destination folder.

    Args:
        input_file (str): The file path to the input MP3 file that will be split.
        destination_folder (str): The directory where the split MP3 chunks will be saved.
        num_chunks (int): The number of chunks to split the MP3 file into.

    Returns:
        None
    """
    # Load the MP3 file
    audio = AudioSegment.from_mp3(input_file)

    # Calculate total duration in milliseconds and the duration of each chunk
    total_duration_ms = len(audio)
    chunk_duration_ms = total_duration_ms / num_chunks

    # Calculate overlap duration in milliseconds (5 seconds)
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

        # Generate filename with start and end timestamps
        filename = f"chunk_{int(start_time)}_{int(end_time)}.mp3"
        full_path = os.path.join(destination_folder, filename)

        # Export the chunk to a new MP3 file
        chunk.export(full_path, format="mp3")

        print(f"Exported {full_path}")


def main():
    """
    Parse command-line arguments and split the MP3 file.

    This function sets up the argument parser to receive input from the command line,
    then calls the `split_mp3` function to perform the MP3 file splitting based on the
    provided arguments.
    """
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Split a large MP3 file into N equal chunks with 5 seconds of overlap."
    )
    parser.add_argument(
        "input_file", type=str, help="The file path to the large MP3 file."
    )
    parser.add_argument(
        "destination_folder",
        type=str,
        help="The destination folder to drop the MP3 chunks.",
    )
    parser.add_argument(
        "num_chunks", type=int, help="The number of chunks to split the file into."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Run the split function with the provided arguments
    split_mp3(args.input_file, args.destination_folder, args.num_chunks)


if __name__ == "__main__":
    main()
