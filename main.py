import streamlit as st
import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

# Fungsi untuk mengubah gambar dari RGB ke HSV
def convert_rgb_to_hsv(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

# Fungsi untuk menghitung histogram
def calculate_histogram(image):
    channels = cv2.split(image)
    colors = ('b', 'g', 'r')
    plt.figure()
    plt.title("Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    for (channel, color) in zip(channels, colors):
        hist = cv2.calcHist([channel], [0], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])
    st.pyplot(plt)

# Fungsi untuk mengubah kecerahan dan kontras
def adjust_brightness_contrast(image, brightness=0, contrast=0):
    beta = brightness - 128
    alpha = contrast / 127 + 1
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted

# Fungsi untuk mendeteksi kontur
def detect_contours(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    return image

# Antarmuka Streamlit
st.title("Aplikasi Manipulasi Gambar Citra")

# Upload gambar
uploaded_file = st.file_uploader("Unggah Gambar", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = np.array(Image.open(uploaded_file))
    st.image(image, caption='Gambar Original', use_column_width=True)

    # Konversi RGB ke HSV
    hsv_image = convert_rgb_to_hsv(image)
    st.image(hsv_image, caption='Gambar dalam HSV', use_column_width=True)

    # Histogram
    st.subheader("Histogram")
    calculate_histogram(image)

    # Kecerahan dan Kontras
    st.subheader("Kecerahan dan Kontras")
    brightness = st.slider("Kecerahan", -128, 128, 0)
    contrast = st.slider("Kontras", -127, 127, 0)
    adjusted_image = adjust_brightness_contrast(image, brightness, contrast)
    st.image(adjusted_image, caption='Gambar dengan Kecerahan dan Kontras yang Disesuaikan', use_column_width=True)

    # Kontur
    st.subheader("Kontur")
    contoured_image = detect_contours(image.copy())
    st.image(contoured_image, caption='Gambar dengan Kontur', use_column_width=True)

