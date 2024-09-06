import numpy as np
import cv2 as cv
import mss
import os
import time
from .utils import find_time, result_format, result_format_codec

file_path = None


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def create_video(fps: int, mp4: bool, screen_size, output_dir: str = "Outputs"):
    mkdir(output_dir)
    file_path = f"{output_dir}/FrameRecorder_{find_time()}{result_format(mp4)}"

    fourcc = cv.VideoWriter_fourcc(*result_format_codec(mp4))
    out = cv.VideoWriter(
        file_path,
        fourcc,
        fps,
        screen_size,
    )
    return out, file_path


def record(out, monitor):
    with mss.mss() as sct:
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        if frame.shape[2] == 4:
            frame = frame[:, :, :3]
        out.write(frame)
