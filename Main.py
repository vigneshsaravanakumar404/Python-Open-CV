# Imports
import numpy
import streamlit
from PIL import Image
from numpy import asarray
from numpy import ndarray

# Functions
def removebg(image: Image, THRESHOLD: int, R: int, G: int, B: int) -> Image:
    image = asarray(image)
    row, col, _ = image.shape
    image = ndarray.tolist(image)


    for r in range(row):
        for c in range(col):
            if sum(image[r][c]) < THRESHOLD:
                image[r][c] = [R, G, B, 255]
            else:
                image[r][c] = [255, 255, 255, 0]

    image = numpy.array(image, dtype=numpy.uint8)
    image = Image.fromarray(image)
    return image

def hex_to_rgb(hex: str) -> tuple:
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

 

# Defaults
THRESHOLD = 300
R, G, B = 0, 0, 0

# Main
streamlit.title("✒️ Signature Background Remover")
THRESHOLD = streamlit.slider('Threshold', 0, 255 * 3, 500, 1)
R, G, B = hex_to_rgb(streamlit.color_picker('Pick A Color', '#FFFFFF'))
IMAGE = removebg(Image.open("messis-signature-small-buttons.png"), THRESHOLD, R, G, B)
streamlit.image(IMAGE)
