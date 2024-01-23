# Imports
import numpy
import streamlit as streamlit
from PIL import Image
from numpy import asarray
from numpy import ndarray

# Functions
def removebg(image: Image, THRESHOLD: int) -> Image:
    image = asarray(image)
    row, col, _ = image.shape
    image = ndarray.tolist(image)


    for r in range(row):
        for c in range(col):
            if sum(image[r][c]) < THRESHOLD:
                image[r][c] = [0, 0, 0, 255]
            else:
                image[r][c] = [255, 255, 255, 0]

    image = numpy.array(image, dtype=numpy.uint8)
    image = Image.fromarray(image)
    return image


# Variables
THRESHOLD = 300
image = removebg(Image.open(r"assets\messis-signature-small-buttons.png"), THRESHOLD)
image.save(r"assets\test.png") 


# Main
streamlit.title("✒️ Signature Background Remover")
