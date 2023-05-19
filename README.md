# PhoneWaver Codec Extension
Setup wizard for FFmpeg's GPL windows binaries taylored towards the needs of our PhoneWaver software.

## Details
This project downloads the latest GPL build of FFmpeg for Windows from [BtbN's FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds/). It uses Inno Setup to compile a setup executable that allows for adding the installation path to the `PATH` variable. PhoneWaver is able to recognize and use the additional codecs provided by the GPL build.

## Usage
To download the latest FFmpeg binaries for Windows use
```bash
./setup.py --download
```
You may dump the server's response with `setup.py --dump` to a file called `.download.zip`.

To compile the installer wizard using Inno Setup use
```bash
./setup.py --compile
```
Please make sure `iscc.exe` is in your PATH enviroment variable.

To execute all the above commands at once, simply leave all arguments:
```bash
./setup.py
```
