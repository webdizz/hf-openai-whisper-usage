import os
import requests
import argparse
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

parser = argparse.ArgumentParser(
    description="Script to distribute Azure publish profiles to github repositories"
)

parser.add_argument("--dir", type=str, help="Path to dir with audio files")
args = parser.parse_args()

dir = args.dir


def transcribe(filename: str):
    audio_ext = os.path.splitext(filename)[1][1:]
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {os.environ['HF_API_TOKEN']}",
        "Content-Type": f"audio/{audio_ext}",
    }

    print("== Transcribing file: %s" % filename)
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(os.environ["HF_API_URL"], headers=headers, data=data)
    if response:
        transcription = response.json()["text"]

        transcription_file = "transcripts/" + os.path.basename(filename) + ".txt"
        print(
            "== Got transcription for file: %s will save into %s"
            % (filename, transcription_file)
        )
        if os.path.exists(transcription_file):
            os.remove(transcription_file)

        with open(transcription_file, "w") as f:
            f.write(str(transcription))
    else:
        print("== Error transcribing file: %s" % filename)


def get_files(dir: str):
    files = []
    for root, _, filenames in os.walk(dir):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


files = sorted(get_files(dir))
for file in files:
    transcribe(file)
