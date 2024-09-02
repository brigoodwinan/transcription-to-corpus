import argparse
import json
import os
from glob import glob
from os.path import join as pjoin
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def translate_gpt(fname: str) -> None:
    with open(fname, "rb") as audio_file:
        translation = client.audio.translations.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
        )

    with open(Path(fname).with_suffix(".json"), "w") as f:
        json.dump(translation.model_dump(), f)


def main():
    parser = argparse.ArgumentParser(
        description="Translate MP3 files using OpenAI GPT."
    )
    parser.add_argument(
        "inputdir",
        type=str,
        help="Fully resolved path to folder containing MP3 files for translation",
    )
    args = parser.parse_args()

    fls = glob(pjoin(args.inputdir, "*mp3"))
    for fname in fls:
        translate_gpt(fname)


if __name__ == "__main__":
    main()
