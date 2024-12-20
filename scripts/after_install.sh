#!/bin/bash
set -e

echo "Navigating to /home/ubuntu/app..."
cd /home/ubuntu/app

echo "Ownership and permissions of /home/ubuntu/app before creating venv:"
ls -ld /home/ubuntu/app

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

# echo "Upgrading pip..."
# sudo apt-get install python3-pip
# pip install --upgrade pip

echo "Installing dependencies from requirements.txt..."
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

echo "Installing liblouis dependencies..."
cd Translation/utils/liblouis-3.31.0
./configure
make
sudo make install
cd python
python setup.py install

echo "Virtual environment setup complete. Python and pip versions:"
which python
python --version
which pip
pip --version
