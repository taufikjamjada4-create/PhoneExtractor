import cv2, os

# All 5 videos
videos = ["Video1.mp4", "Video2.mp4", "Video3.mp4", "Video4.mp4", "Video5.mp4"]

output_folder = "frames"
os.makedirs(output_folder, exist_ok=True)

total_saved = 0

for video_path in videos:
    print(f"Processing {video_path}...")
    
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % fps == 0:
            filename = f"{output_folder}/frame_{total_saved:04d}.jpg"
            cv2.imwrite(filename, frame)
            total_saved += 1
        frame_count += 1

    cap.release()
    print(f"Done with {video_path}")

print(f"\nAll videos done! Total frames saved: {total_saved}")