# Imports
import cv2
import streamlit as st
import numpy as np
from io import BytesIO

# Functions
import numpy as np
import cv2

def removebg(image: np.ndarray, THRESHOLD: int, color: tuple) -> np.ndarray:

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Convert to RGB
    row, col, _ = image.shape # Determine Demensions
    transparent_img = np.zeros((row, col, 4), dtype=np.uint8) # Create an empty image with 4 channels
    
    # Iterate through each pixel and check if the sum of the pixel values is less than the threshold
    for r in range(row):
        for c in range(col):
            if sum(image[r][c]) < THRESHOLD:
                transparent_img[r, c] = [*color, 255]
            else:
                transparent_img[r, c] = [0, 0, 0, 0]

    return transparent_img

# Convert HEX to RGB: https://stackoverflow.com/q/29643352
def hex_to_rgb(value: str) -> tuple:
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# Download Button
def get_image_download_link(img, filename: str, text: str) -> st.download_button:
    
    # Convert to PNG
    _, encoded_image = cv2.imencode('.png', img)
    encoded_image = encoded_image.tobytes()

    # Generate download button
    return st.download_button(
            label=text,
            data=encoded_image,
            file_name=filename,
            mime="image/png"
    )

# UI Enhancements
st.title("✒️ Signature Background Remover")
st.markdown("Easily remove the background from your signature and customize its color. Just upload your image, adjust the settings, and download your new signature!")

# Layout Adjustments
col1, col2 = st.columns(2)
with col1:
    INPUT = st.file_uploader("Choose an Image File", type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)
with col2:
    COLOR_HEX = st.color_picker('Pick A Signature Color', '#000000')
    THRESHOLD = st.slider('Threshold', 0, 255 * 3, 300, 1)

if INPUT is not None:
    FILE = np.asarray(bytearray(INPUT.read()), dtype=np.uint8)
    R, G, B = hex_to_rgb(COLOR_HEX)
    IMAGE = removebg(cv2.imdecode(FILE, cv2.IMREAD_COLOR), THRESHOLD, (R, G, B))
    st.image(IMAGE, use_column_width=True, channels="RGBA")
    get_image_download_link(IMAGE, "modified_signature.png", "Download Modified Signature")
else:
    st.warning("Please upload an image file")

st.sidebar.header("How It Works")
st.sidebar.text("1. Upload your signature image.\n2. Adjust the threshold and color.\n3. Download your modified signature.")

st.sidebar.header("About")
st.sidebar.info("By: Vignesh Saravanakumar")
