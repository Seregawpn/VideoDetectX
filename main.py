import cv2
import numpy as np
import argparse
import json
import os
import sys
from datetime import datetime


def detect_camera_shake(video_path, output_path, threshold=0.5):
    """
    Detects camera shake in a video using optical flow.
    
    Args:
        video_path: Path to the input video file
        output_path: Path to save the results
        threshold: Threshold for motion detection
        
    Returns:
        A list of timestamps where camera shake was detected
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return []
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Read first frame
    ret, prev_frame = cap.read()
    if not ret:
        print("Error: Could not read first frame")
        return []
    
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    
    # Results storage
    shake_timestamps = []
    frame_count = 1
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate optical flow using Farneback method
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        
        # Calculate magnitude and angle of flow vectors
        magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        
        # Get mean magnitude of motion
        mean_magnitude = np.mean(magnitude)
        
        # If motion is above threshold, consider it camera shake
        if mean_magnitude > threshold:
            timestamp = frame_count / fps
            shake_timestamps.append({
                "frame": frame_count,
                "timestamp": timestamp,
                "magnitude": float(mean_magnitude)
            })
            
        # Update previous frame
        prev_gray = gray
        frame_count += 1
    
    cap.release()
    
    # Save results to file
    with open(output_path, 'w') as f:
        json.dump({
            "source_video": video_path,
            "shake_events": shake_timestamps,
            "total_events": len(shake_timestamps)
        }, f, indent=2)
    
    return shake_timestamps


def detect_faces_objects(video_path, output_path, cascade_type='face'):
    """
    Detects faces or objects in a video using Haar cascade.
    
    Args:
        video_path: Path to the input video file
        output_path: Path to save the results
        cascade_type: Type of detection ('face' or 'object')
        
    Returns:
        A list of frames and counts where faces/objects were detected
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return []
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Load appropriate cascade classifier
    if cascade_type == 'face':
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    elif cascade_type == 'object':
        cascade_path = cv2.data.haarcascades + 'haarcascade_fullbody.xml'
    else:
        print(f"Error: Unknown cascade type '{cascade_type}'")
        return []
    
    # Load cascade classifier
    cascade = cv2.CascadeClassifier(cascade_path)
    
    # Results storage
    detection_results = []
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces/objects
        detections = cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(detections) > 0:
            timestamp = frame_count / fps
            detection_results.append({
                "frame": frame_count,
                "timestamp": timestamp,
                "count": len(detections),
                "locations": detections.tolist() if len(detections) > 0 else []
            })
        
        frame_count += 1
    
    cap.release()
    
    # Save results to file
    with open(output_path, 'w') as f:
        json.dump({
            "source_video": video_path,
            "detection_type": cascade_type,
            "detections": detection_results,
            "total_frames_with_detections": len(detection_results)
        }, f, indent=2)
    
    return detection_results


def main():
    parser = argparse.ArgumentParser(description="Video Analysis Tool")
    parser.add_argument("video", help="Path to the input video file")
    parser.add_argument("--mode", choices=["shake", "face", "object"], default="shake",
                        help="Detection mode: camera shake, face, or object detection")
    parser.add_argument("--output", help="Path to save the output JSON file")
    parser.add_argument("--threshold", type=float, default=0.5,
                        help="Motion threshold for camera shake detection (default: 0.5)")
    
    args = parser.parse_args()
    
    # Check if video file exists
    if not os.path.isfile(args.video):
        print(f"Error: Video file '{args.video}' not found")
        sys.exit(1)
    
    # Set default output path if not provided
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"{os.path.splitext(args.video)[0]}_{args.mode}_{timestamp}.json"
    
    print(f"Analyzing video: {args.video}")
    print(f"Mode: {args.mode}")
    print(f"Output will be saved to: {args.output}")
    
    if args.mode == "shake":
        results = detect_camera_shake(args.video, args.output, args.threshold)
        print(f"Analysis complete. Found {len(results)} camera shake events.")
    elif args.mode == "face":
        results = detect_faces_objects(args.video, args.output, "face")
        print(f"Analysis complete. Found faces in {len(results)} frames.")
    elif args.mode == "object":
        results = detect_faces_objects(args.video, args.output, "object")
        print(f"Analysis complete. Found objects in {len(results)} frames.")
    
    print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()
