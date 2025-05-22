
#continuosly pulls frames from hls stream and saves them to the disk
#used openCV to open the stream URL and capture one frame every INTERVAL seconds

import os
import cv2
import time
import yaml

#load configuration from config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

STREAM_URL = config['url'] # "https://edge02.nginx.hdontap.com/hosb3/hdontap_carlsbad_terra-mar-pt.stream/chunklist_w1792613303_vo.m3u8"
INTERVAL = config['interval'] # 5 how often to save a frame
OUT_DIR = config['data_dir', "data/raw frames"] # "data/raw frames" # directory to save frames

#prepare output directory
os.makedirs(OUT_DIR, exist_ok=True)

# open stream once at startup
#videocapture will reconnect automatically on HLS segment change
cap = cv2.VideoCapture(STREAM_URL)
if not cap.isOpened():
    raise RuntimeError(f"Could not open stream: {STREAM_URL}")\

print(f"🎥 Scraping frames every {INTERVAL}s into '{OUT_DIR}/'")

#main loop to grab and save frames indefinitely
try:
    while True:
        #read a single frame from stream
        ret, frame = cap.read()
        ts = int(time.time())
        if ret:
            #build filename with current UNIX timestamp
            filename = os.path.join(OUT_DIR, f"{ts}.jpg")
            #write frame to disk as JPEG
            cv2.inwrite(filename, frame)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Saved frame to {filename}")
            else:
                #handle occasional read failure by logging anf retrying
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Failed to grab a frame, retrying..")
                #wait for the next capture interval
            time.sleep(INTERVAL)
            finally:
                #clean up by releasing videocapture on exit
                cap.release()
                print("Stream closed.")




