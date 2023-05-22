#!/usr/bin/env python

import fnmatch
import pathlib
import shutil
import subprocess
import zipfile

from argparse import ArgumentParser
from io import BytesIO

import tqdm
import requests



FFMPEG_EXTRACT_PATH = pathlib.Path(__file__).parent / "workdir" / "ffmpeg"

parser = ArgumentParser()
parser.add_argument("--download", action="store_true")
parser.add_argument("--compile", action="store_true")
parser.add_argument("--dump", action="store_true")



def download(url:str, dump:bool) -> None:
    content = bytearray()

    # request a download
    r = requests.get(url, allow_redirects=True, stream=True)

    pbar_settings = {
        "desc": "Download",
        "total": int(r.headers.get("content-length", 0)),
        "unit": "iB",
        "unit_scale": True,
    }

    # buffer download into content bytearray and visualize with progress bar
    with tqdm.tqdm(**pbar_settings) as pbar:
        for data in r.iter_content(1024):
            pbar.update(len(data))
            content.extend(data)

    # dump to zip file if needed
    if dump:
        with open(".download.zip", "wb") as dumpfile:
            dumpfile.write(content)

    # delete existing download
    if FFMPEG_EXTRACT_PATH.exists():
        shutil.rmtree(FFMPEG_EXTRACT_PATH)

    # open downloaded zip data
    with zipfile.ZipFile(BytesIO(content)) as z:
        main_folder = fnmatch.filter(z.namelist(), "*/")[0]

        # extract everything from first child directory
        for zipinfo in tqdm.tqdm(z.infolist(), desc="Extract"):
            file_name = zipinfo.filename

            if file_name == main_folder:
                continue # if file/dir is main folder
            if not file_name.startswith(main_folder):
                continue # if file/dir is not from main folder, e.g. siblings

            zipinfo.filename = file_name.replace(main_folder, "")
            z.extract(zipinfo, FFMPEG_EXTRACT_PATH)

    # add prefix to main executables to avoid conflicts when added to PATH
    bin_dir = FFMPEG_EXTRACT_PATH / "bin"
    if bin_dir.exists():
        for element in bin_dir.iterdir():
            if not element.is_file():
                continue
            element.rename(element.with_stem(f"phonewaver-{element.stem}"))



def inno_compile():
    if shutil.which("iscc") is None:
        raise FileNotFoundError("iscc.exe not found in PATH environment variable.")

    if not FFMPEG_EXTRACT_PATH.exists():
        raise FileNotFoundError(
            "Binary files are missing. "
            "Please download first with --download flag "
            "or leave all flags to download and compile in one step."
        )

    subprocess.run(["iscc", "installer.iss"])



def main():
    args = parser.parse_args()
    all = not any((args.download, args.compile)) # if none given, execute all

    if args.download or all:
        repo = "https://github.com/BtbN/FFmpeg-Builds/"
        file = "ffmpeg-n6.0-latest-win64-gpl-6.0.zip"
        download(f"{repo}releases/download/latest/{file}", args.dump)

    if args.compile or all:
        inno_compile()



if __name__ == "__main__":
    main()
