# AI Virtual Mouse 🖱️

A real-time AI-based virtual mouse that allows users to control their computer using hand gestures and eye blinks.

This system uses computer vision to track hand landmarks and eye movements, enabling cursor movement, left click, right click, and scrolling without touching a physical mouse.

## Features
- Hand gesture based cursor movement
- Eye blink based left click
- Two-finger scroll
- Thumb–index pinch for right click
- Live hand skeleton & fingertip tracking
- No external hardware required

## Technologies Used
- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- Computer Vision
- Human–Computer Interaction (HCI)

## How It Works
The webcam captures live video frames which are processed using MediaPipe to detect hand and eye landmarks.  
Finger positions are mapped to screen coordinates for cursor movement.  
Eye blink detection triggers mouse clicks.  
Gesture recognition enables scrolling and right-click actions.

## Installation
```bash
pip install -r requirements.txt

## Run
```bash
python virtual_mouse_full.py

## Use Cases
- Touchless computing
- Assistive technology
- AR/VR and HCI systems
- Hands-free computer control

## Author
- Poojitha Mavuri