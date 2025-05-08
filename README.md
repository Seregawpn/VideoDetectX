# VideoDetectX

Lightweight video analysis tools for camera shake detection and object recognition.

## Features

- **Camera Shake Detection**: Uses optical flow to identify abrupt camera movements
- **Face Recognition**: Uses Haar cascade classifier for detecting faces
- **Object Detection**: Uses Haar cascade classifier for detecting objects

## Usage

```bash
python main.py video.mp4 --mode shake --output results.json --threshold 0.5
python main.py video.mp4 --mode face --output faces.json
python main.py video.mp4 --mode object --output objects.json
```

### Parameters

- `video`: path to the video file for analysis
- `--mode`: analysis mode (`shake`, `face`, or `object`)
- `--output`: file to save results (default is automatically generated)
- `--threshold`: threshold for camera shake detection (default is 0.5)

## Output Format

Results are saved in JSON format:

### For camera shake detection:
```json
{
  "source_video": "video.mp4",
  "shake_events": [
    {
      "frame": 45,
      "timestamp": 1.5,
      "magnitude": 1.23
    },
    ...
  ],
  "total_events": 12
}
```

### For face/object detection:
```json
{
  "source_video": "video.mp4",
  "detection_type": "face",
  "detections": [
    {
      "frame": 30,
      "timestamp": 1.0,
      "count": 2,
      "locations": [[x, y, width, height], ...]
    },
    ...
  ],
  "total_frames_with_detections": 45
}
```

## Creating Standalone Executables

### For Windows:
```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

### For macOS:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

You can also use the included build script:
```bash
python build.py
```

Executable files will be created in the `dist` directory. 