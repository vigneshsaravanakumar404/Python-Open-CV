# Imports
import cv2
import streamlit as st
import numpy as np

# Functions
def removebg(image, THRESHOLD: int, R: int, G: int, B: int) -> np.ndarray:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    row, col, _ = image.shape
    
    for r in range(row):
        for c in range(col):
            if sum(image[r][c]) < THRESHOLD:
                image[r][c] = [R, G, B]
            else:
                image[r][c] = [255, 255, 255]

    return image

def hex_to_rgb(hex: str) -> tuple:
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

# Main section
st.title("✒️ Signature Background Remover")
INPUT = st.file_uploader("Choose an Image File", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)
THRESHOLD = st.slider('Threshold', 0, 255 * 3, 300, 1)
COLOR_HEX = st.color_picker('Pick A Color', '#000000')
R, G, B = hex_to_rgb(COLOR_HEX)

if INPUT is not None:
    file_bytes = np.asarray(bytearray(INPUT.read()), dtype=np.uint8)
    IMAGE = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    # Display the processed image
    st.image(removebg(IMAGE, THRESHOLD, R, G, B), use_column_width=True)
else:
    st.write("Please Upload an Image")
