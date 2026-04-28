import cv2
import numpy as np

def apply_watermark(input_video, output_video):
    cap = cv2.VideoCapture(input_video)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    watermark_strength = 5

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to YCrCb (separates brightness)
        ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(ycrcb)

        # Apply DCT on Y channel only
        y = np.float32(y)
        dct = cv2.dct(y)

        # Embed watermark
        dct[10:20, 10:20] += watermark_strength

        # Inverse DCT
        idct = cv2.idct(dct)

        y = np.uint8(np.clip(idct, 0, 255))

        # Merge back
        watermarked = cv2.merge((y, cr, cb))
        final_frame = cv2.cvtColor(watermarked, cv2.COLOR_YCrCb2BGR)

        out.write(final_frame)

    cap.release()
    out.release()

def detect_watermark(video_path):
    cap = cv2.VideoCapture(video_path)

    watermark_detected = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        y, _, _ = cv2.split(ycrcb)

        y = np.float32(y)
        dct = cv2.dct(y)

        # Check watermark region
        region = dct[10:20, 10:20]

        # If values are high → watermark present
        if np.mean(region) > 50:
            watermark_detected = True
            break

    cap.release()
    return watermark_detected