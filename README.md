# Purpose

This repo contains scripts and tools for data preparation and postprocessing for audio transcription or translation tasks using openAI APIs.

# Running Scripts individually

| Run Sequence | Script                          | Description                                                                                             | Arguments                                              |
|--------------|---------------------------------|---------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| 1            | `bash ./convert_mp4_to_mp3_folder.sh`   | Converts all MP4 files in the source folder to MP3 format and saves them in the destination folder.      | `<source_folder> <destination_folder>`                 |
| 2            | `python ./mp3_into_25mb_chunks_folder.py` | Splits each MP3 file in the folder into smaller chunks, each less than 25MB, with a 5-second overlap between chunks. | `<folder_path> --max_chunk_size_mb <max_chunk_size_mb>` |
| 3            | `bash ./process_subfolders_of_mp3s.sh`  | Processes each subfolder containing MP3 chunks, running the transcription script on each chunk to generate JSON and TXT transcriptions. | `<parent_folder>`                                      |
| 4            | `bash ./concatenate_text_files.sh`      | Concatenates all text files in the source folder into a single output file, adding file separators between each file's content. | `<source_folder> <output_file>`                        |

# Master script

`master_script.sh` was generated automatically and not tested, but it should run the entire pipeline end-to-end for a folder containing mp4 files.

### Explanation:

- **Arguments**: The script now expects four command-line arguments:
  1. `source_mp4_folder`: Path to the folder containing the original MP4 files.
  2. `destination_mp3_folder_and_parent_folder`: Path to the folder where the converted MP3 files will be saved, and which will also be used as the parent folder for processing subfolders.
  3. `max_chunk_size_mb`: Maximum size of each MP3 chunk in megabytes.
  4. `output_text_file`: Path to the output file where all text files will be concatenated.

### Running the Script:

To execute the updated script, save it as `master_script.sh`, give it execute permissions, and run it like this:

```bash
chmod +x master_script.sh
./master_script.sh /path/to/source_mp4 /path/to/destination_folder 25 /path/to/output_text_file.txt
```

This script will handle the entire workflow, including converting MP4 files to MP3, splitting the MP3 files, processing subfolders for transcription, and finally concatenating all text files into a single output file.