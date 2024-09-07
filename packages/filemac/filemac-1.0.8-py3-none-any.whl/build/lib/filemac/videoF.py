import cv2
import numpy as np


def detect_missing_frames(frames):
    # A dummy implementation for missing frame detection
    # In real scenarios, this might involve checking frame indexes, hashes, etc.
    missing_frames = []
    for i in range(1, len(frames) - 1):
        if frames[i] is None:
            missing_frames.append(i)
    print(f"Found {len(missing_frames)} missing frames")
    return missing_frames


def interpolate_frame(prev_frame, next_frame):
    return cv2.addWeighted(prev_frame, 0.5, next_frame, 0.5, 0)


def repair_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    frames = []
    for _ in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            frames.append(None)
        else:
            frames.append(frame)

    cap.release()

    missing_frames = detect_missing_frames(frames)
    if len(missing_frames) > frame_count * 0.1:  # Arbitrary threshold for many missing frames
        frames = [f for f in frames if f is not None]
    else:
        for i in missing_frames:
            if i > 0 and i < frame_count - 1 and frames[i-1] is not None and frames[i+1] is not None:
                frames[i] = interpolate_frame(frames[i-1], frames[i+1])
            else:
                frames[i] = frames[i-1] if frames[i -
                                                  1] is not None else frames[i+1]

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(
        *'mp4v'), fps, (width, height))

    for frame in frames:
        if frame is not None:
            out.write(frame)

    out.release()
    print("Video repair complete and saved to:", output_path)


# Usage
input_video_path = '/home/skye/Videos/sweet home/Sweet Home S01E10 1080p ENGLISH.mp4'
output_video_path = 'output_video.mp4'
repair_video(input_video_path, output_video_path)
