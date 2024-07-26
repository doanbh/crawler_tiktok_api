import re
import cv2
import numpy as np
from io import BytesIO
import requests

def is_instagram_link(link):
    # Regular expression pattern for Instagram video links
    pattern = r'^https?:\/\/(?:www\.)?instagram\.com\/(?:p|reel)\/[a-zA-Z0-9_-]+\/?(?:\?.*)?$'
    
    # Check if the link matches the pattern
    if re.match(pattern, link):
        return True
    else:
        return False
    
def get_first_frame(video_url):
    video_data = requests.get(video_url, stream=True).raw
    video_bytes = video_data.read()
    video_array = np.asarray(bytearray(video_bytes), dtype=np.uint8)
    video = cv2.VideoCapture(BytesIO(video_array))
    
    success, frame = video.read()
    if success:
        return frame
    else:
        return None
    
# save image
def save_image(image, path):
    if image is not None:
        # Save the frame to an image file
        cv2.imwrite("first_frame.jpg", image)
        print("First frame saved as 'first_frame.jpg'")
    else:
        print("Failed to retrieve the first frame.")