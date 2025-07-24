import os
import cv2
import yt_dlp
import json
from pathlib import Path


def load_config(path='config.json'):
    with open(path, 'r') as f:
        return json.load(f)


def download_youtube_video(url, output_path="video.mp4"):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': output_path,
        'overwrites': True,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def extract_frames(video_path, output_folder, every_n_frames=30):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Could not open video file: {video_path}")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames: {total_frames}")

    Path(output_folder).mkdir(parents=True, exist_ok=True)
    count = 0
    saved = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % every_n_frames == 0:
            frame_path = os.path.join(output_folder, f"frame_{saved:05d}.jpg")
            cv2.imwrite(frame_path, frame)
            saved += 1
        count += 1

    cap.release()
    print(f"Saved {saved} frames.")


def main():
    config = load_config()

    source_type = config.get("video_source_type")
    video_file = config["video_file"]
    frame_output_dir = config["frame_output_dir"]
    every_n_frames = config.get("every_n_frames")

    if source_type == "url":
        video_url = config["video_url"]
        print(f"Downloading video from URL: {video_url}")
        download_youtube_video(video_url, video_file)
    else:
        print(f"Using local video file: {video_file}")

    extract_frames(video_file, frame_output_dir, every_n_frames)


if __name__ == "__main__":
    main()
