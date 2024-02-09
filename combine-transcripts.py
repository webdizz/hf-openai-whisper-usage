import os
import argparse
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

parser = argparse.ArgumentParser(
    description="Script to combine transcripts into one file"
)

parser.add_argument("--dir", type=str, help="Path to dir with transcript files")
args = parser.parse_args()

dir = args.dir

if not dir:
    dir = "./transcripts"


def get_files(dir: str):
    files = []
    for root, _, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(".txt"):
                files.append(os.path.join(root, filename))
    return files


def read_file(file: str, current_file_content: str):
    with open(file, "r") as f:
        current_file_content += f.read()
    return current_file_content


files = sorted(get_files(dir))
current_file_group = ""
current_file_content = ""
for file in files:
    file_name_parts = file.split("_")
    file_group_name = "_".join(file_name_parts[:-1])
    print(file_group_name)
    if current_file_group == "":
        current_file_group = file_group_name
        current_file_content = read_file(file, current_file_content)
    elif file_group_name == current_file_group:
        current_file_content = read_file(file, current_file_content)
    else:
        if current_file_group != "":
            with open(current_file_group + ".exp", "w") as f:
                f.write(current_file_content)
            current_file_group = file_group_name
            current_file_content = read_file(file, "")