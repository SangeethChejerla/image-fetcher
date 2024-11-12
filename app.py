import io
import os
from urllib.parse import urlparse

import requests
import streamlit as st
from PIL import Image


def download_image(url, save_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Use PIL to open the image from the response content
        image = Image.open(io.BytesIO(response.content))

        # Ensure the file extension is .jpg or .png
        if save_path.lower().endswith((".png", ".jpg")):
            image_format = save_path.split(".")[-1].lower()
        else:
            image_format = "png"  # Default to PNG for better quality
            save_path += ".png"

        # Create directory if it doesn't exist
        os.makedirs(
            os.path.dirname(save_path) if os.path.dirname(save_path) else ".",
            exist_ok=True,
        )

        # Save the image
        image.save(save_path, format=image_format)

        st.success(f"Image successfully downloaded and saved as {save_path}")
        return True

    except requests.exceptions.RequestException as e:
        st.error(f"Error downloading image: {e}")
        return False
    except Exception as e:
        # Handle specific image format errors
        if "JPG" in str(e):
            st.error("The image might not be in a recognized format. Saving as PNG.")
            save_path = (
                save_path.rsplit(".", 1)[0] + ".png"
                if "." in save_path
                else save_path + ".png"
            )
            image.save(save_path, format="png")
            st.success(f"Image saved as {save_path}")
            return True
        else:
            st.error(f"An error occurred while processing the image: {e}")
            return False


# Streamlit app
st.title("Image Downloader")

# Input for URL
url = st.text_input("Enter Image URL:")

# Input for filename
filename = st.text_input("Enter Filename (optional):")

# Download button
if st.button("Download Image"):
    if url:
        save_path = (
            filename if filename else os.path.basename(urlparse(url).path) or "image"
        )
        download_image(url, save_path)
    else:
        st.warning("Please enter an image URL.")
