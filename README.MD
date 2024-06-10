# Create Korean Notes

## Project

This project is a python script made for my own use to create and import Korean language Anki notes.

## Setting up

### Linux

#### Prerequisites

Make sure you comply with the following requirements:
- Python 3 is installed on your system. I am using version 3.12.3
- pip is installed on your system. I am using verison 24.0

If all this is okay then you can run the following commands :
```console
# Install venv (python 3.12):
sudo apt install python3.12-venv

# Create the virtual environment:
# NB: If you do not name it '.venv' please add your virtual environment folder to your git exclude file. [See documentation here](https://git-scm.com/docs/gitignore)
python3 -m venv .venv

# Enter the virtual environment:
source .venv/bin/activate

# Installing the requirements:
pip install -r requirements.txt

# Do what you have to do : Coding, generating notes, etc.
# ...
# ...

# Leave the virtual environment:
deactivate
```

## Generate Notes

To generate notes use `python3 ./main.py` while being in the virtual environment.
