# Improved Streamlit App for Signature Background Removal
import streamlit as st
import numpy as np
import cv2

# Function to remove background based on a threshold
def removebg(image: np.ndarray, THRESHOLD: int, color: tuple) -> np.ndarray:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    row, col, _ = image.shape  # Get image dimensions
    transparent_img = np.zeros((row, col, 4), dtype=np.uint8)  # Prepare a transparent image
    
    for r in range(row):
        for c in range(col):
            if sum(image[r][c]) < THRESHOLD:  # Check pixel value against threshold
                transparent_img[r, c] = [*color, 255]  # Set new pixel value
            else:
                transparent_img[r, c] = [0, 0, 0, 0]  # Make pixel transparent

    return transparent_img

# Function to convert HEX color to RGB
def hex_to_rgb(value: str) -> tuple:
    value = value.lstrip('#')
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))

# Function to generate Download Button
def get_image_download_link(img, filename: str, text: str):
    _, encoded_image = cv2.imencode('.png', img) # Convert to PNG
    encoded_image = encoded_image.tobytes() # Convert to bytes
    return st.download_button(label=text, data=encoded_image, file_name=filename, mime="image/png") # Download button

# UI
st.title("✒️ Signature Background Remover")

# Sidebar for settings and instructions
with st.sidebar:
    st.header("How It Works")
    st.write("""
    1. Upload your signature image.
    2. Adjust the threshold and color.
    3. Download your modified signature.
    """)
    st.header("Settings")
    INPUT = st.file_uploader("Choose an Image File", type=['png', 'jpg', 'jpeg'])
    COLOR_HEX = st.color_picker('Signature Color', '#000000')
    THRESHOLD = st.slider('Threshold', 0, 255 * 3, 300, 1)

    

# Processing and Display
if INPUT is not None:
    FILE = np.asarray(bytearray(INPUT.read()), dtype=np.uint8)
    R, G, B = hex_to_rgb(COLOR_HEX)
    IMAGE = removebg(cv2.imdecode(FILE, cv2.IMREAD_COLOR), THRESHOLD, (R, G, B))
    
    st.image(IMAGE, use_column_width=True, channels="RGBA")
    get_image_download_link(IMAGE, "modified_signature.png", "Download Modified Signature")
else:
    st.empty()  # Optionally show guidance

# About section in sidebar
st.sidebar.header("About")
st.sidebar.info("By: Vignesh")
