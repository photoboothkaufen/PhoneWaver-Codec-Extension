# FFmpeg Windows Installer
Setup wizard for FFmpeg using Inno Setup. Doesn't reinvent the wheel.

## Details
This script downloads the latest GPL build of FFmpeg for x64 Windows from [BtbN's FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds/). It uses Inno Setup to compile a setup executable that allows for adding the installation path to the `PATH` variable.

## Usage
To download the latest GPL FFmpeg binaries for Windows use
```bash
./setup.py --download
```
You may dump the download server's response with `setup.py --dump` to a file called `.download.zip`.

To compile a installer wizard using Inno Setup use
```bash
./setup.py --compile
```
Please make sure `iscc.exe` is in your PATH enviroment variable.

To execute all the above commands at once, simply leave all arguments:
```bash
./setup.py
```
