
#continuosly pulls frames from hls stream and saves them to the disk
#used openCV to open the stream URL and capture one frame every INTERVAL seconds

import os
import cv2
import time
import yaml

#load configuration from config.yaml
with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

STREAM_URL = cfg["camera"]["url"] # "https://edge02.nginx.hdontap.com/hosb3/hdontap_carlsbad_terra-mar-pt.stream/chunklist_w1792613303_vo.m3u8"
INTERVAL = cfg["camera"]["capture_interval"] # 5 how often to save a frame
OUT_DIR = cfg.get("data_dir", "data/raw frames") # "data/raw frames" # directory to save frames

#prepare output directory
os.makedirs(OUT_DIR, exist_ok=True)

# open stream once at startup
#videocapture will reconnect automatically on HLS segment change
os.makedirs(OUT_DIR, exist_ok=True)
print(f"🎥 Grabbing one fresh frame every {INTERVAL}s")

#main loop to grab and save frames indefinitely
try:
    while True:
        #read a single frame from stream
        cap = cv2.VideoCapture(STREAM_URL)
        if not cap.isOpened():
            print("Error: Could not open video stream.")
            break
        else:
            ret, frame = cap.read()
            cap.release()
            if ret and frame is not None:
                #save frame to disk
                ts = int(time.time())
                fn = os.path.join(OUT_DIR, f"frame_{ts}.jpg")
                cv2.imwrite(fn, frame)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Saved frame to {fn}")
            else:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Failed to grab a frame")
        time.sleep(INTERVAL) #wait for the next interval
except KeyboardInterrupt:
    print("Stream capture interrupted by user.")




