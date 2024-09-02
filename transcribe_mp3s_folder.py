import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def transcribe_audio(file_path: str, output_json: str, output_txt: str) -> None:
    """
    Transcribe an audio file and save the results in JSON and TXT formats.

    This function takes an MP3 file, sends it to a transcription service, and
    saves the detailed transcription as a JSON file. Additionally, it extracts
    the plain text from the transcription and saves it as a TXT file.

    Args:
        file_path (str): The file path to the audio file to be transcribed.
        output_json (str): The file path where the transcription JSON should be saved.
        output_txt (str): The file path where the plain text transcription should be saved.

    Returns:
        None
    """

    print(f"beginning transcription for {file_path}.")

    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            temperature=0.3,
        )

    mod = transcription.model_dump()

    # Save the full transcription as a JSON file
    with open(output_json, "w") as json_file:
        json.dump(mod, json_file, indent=4)

    # Extract and save only the text to a TXT file
    text_output = "\n".join([segment["text"] for segment in mod["segments"]])
    with open(output_txt, "w") as txt_file:
        txt_file.write(text_output)

    print(f"Transcription completed for {file_path}: {output_json}, {output_txt}")


def process_folder_for_transcription(folder_path: str) -> None:
    """
    Process a folder of MP3 files, transcribing each and saving the results.

    This function iterates through all MP3 files in a specified folder (including
    subfolders), transcribes each file, and saves the results as JSON and TXT files
    in the same directory as the original audio file.

    Args:
        folder_path (str): The path to the folder containing MP3 files.

    Returns:
        None
    """
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".mp3"):
                file_path = os.path.join(root, file_name)
                base_name = os.path.splitext(file_name)[0]
                output_json = os.path.join(root, f"{base_name}.json")
                output_txt = os.path.join(root, f"{base_name}.txt")

                transcribe_audio(file_path, output_json, output_txt)


def main():
    """
    Parse command-line arguments and process the folder for transcription.

    This function sets up an argument parser to receive the folder path from the
    command line, and then it calls `process_folder_for_transcription` to handle
    the transcription of all MP3 files in the folder.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Process a folder of MP3 files, transcribing each and saving as JSON and TXT."
    )
    parser.add_argument(
        "folder_path", type=str, help="The path to the folder containing MP3 files."
    )

    args = parser.parse_args()

    process_folder_for_transcription(args.folder_path)


if __name__ == "__main__":
    main()
