#!/bin/bash
./build.sh  # Run the build script to install PortAudio
source venv/bin/activate
pip install -r requirements.txt  # Ensure dependencies are installed
python app.py  # Run the Flask app
