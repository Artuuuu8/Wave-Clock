import cv2

url = "https://edge02.nginx.hdontap.com/hosb3/hdontap_carlsbad_terra-mar-pt.stream/chunklist_w1792613303_vo.m3u8"

cap = cv2.VideoCapture(url)
ret, frame = cap.read()
print("Frame grabbed?", ret)
if ret:
    print("Frame shape:", frame.shape)
    #save sample frame
    cv2.imwrite("sample_frame.jpg", frame)
else:
    print("Failed to grab a frame")
