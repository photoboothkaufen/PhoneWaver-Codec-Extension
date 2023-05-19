#!/usr/bin/env python

import argparse
import fnmatch
import io
import shutil
import subprocess

from pathlib import Path
from zipfile import ZipFile

import requests


parser = argparse.ArgumentParser()
parser.add_argument("--download", action="store_true")
parser.add_argument("--compile", action="store_true")
parser.add_argument("--dump", action="store_true")



def download(url:str, dump:bool) -> None:
    r = requests.get(url, allow_redirects=True)

    if dump:
        with open(".download.zip", "wb") as dumpfile:
            dumpfile.write(r.content)

    with ZipFile(io.BytesIO(r.content)) as z:
        main_folder = fnmatch.filter(z.namelist(), "*/")[0]
        for zipinfo in z.infolist():
            # remove main_folder prefix
            if zipinfo.filename == main_folder:
                continue

            zipinfo.filename = zipinfo.filename.replace(main_folder, "")
            z.extract(zipinfo, Path(__file__).parent / "workdir" / "ffmpeg")



def main():
    args = parser.parse_args()
    all = not any((args.download, args.compile)) # if none given, execute all

    if args.download or all:
        repo = "https://github.com/BtbN/FFmpeg-Builds/"
        file = "ffmpeg-n6.0-latest-win64-gpl-6.0.zip"
        download(f"{repo}releases/download/latest/{file}", args.dump)

    if args.compile or all:
        if shutil.which("iscc") is None:
            raise FileNotFoundError("iscc.exe not found in PATH environment variable.")
        subprocess.run(["iscc", "installer.iss"])



if __name__ == "__main__":
    main()
