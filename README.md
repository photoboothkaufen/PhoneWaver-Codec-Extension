# FFmpeg Windows Installer
Setup wizard for FFmpeg using Inno Setup

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
