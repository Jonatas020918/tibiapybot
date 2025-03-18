# TibiaPyBot

A Python-based bot for Tibia that uses screen identification for automated hunting and looting.

## Features

- Screen-based game element recognition
- Automated hunting system
- Loot collection
- Character status monitoring
- Safety features and emergency responses
- Multiple hunting spot support
- Experience tracking
- Path recording and playback
- User-friendly GUI interface

## Requirements

- Python 3.8 or higher
- OpenCV
- PyAutoGUI
- Tesseract OCR
- Other dependencies listed in requirements.txt

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Jonatas020918/tibiapybot.git
cd tibiapybot
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR on your system:
   - Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt-get install tesseract-ocr`
   - Mac: `brew install tesseract`

## Usage

1. Run the bot GUI:
```bash
python tibia_bot_gui.py
```

2. Configure your settings:
   - General settings (character name, world)
   - Hunting settings (spots, monsters)
   - Potion settings
   - Backpack settings
   - Safety settings

3. Record hunting paths:
   - Go to the Paths tab
   - Click "Record New Path"
   - Move your character
   - Stop recording when done

4. Start hunting:
   - Select your recorded path
   - Click "Play Selected"
   - Monitor the bot through the log window

## Safety Notice

This bot is for educational purposes only. Please check Tibia's terms of service regarding bot usage on your server.

## Project Structure

- `main.py`: Main bot entry point
- `screen_recognition.py`: Screen capture and image processing
- `game_control.py`: Mouse and keyboard control
- `safety.py`: Safety features and emergency responses
- `hunting.py`: Hunting logic and monster detection
- `looting.py`: Loot detection and collection
- `config.py`: Configuration settings
- `monsters.py`: Monster database
- `hunting_spots.py`: Hunting spots database
- `path_recorder.py`: Path recording and playback
- `tibia_bot_gui.py`: Main GUI interface

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 