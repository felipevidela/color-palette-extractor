import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

st.set_page_config(page_title="Color Palette Extractor", layout="wide")
st.title("Color Palette Extractor")

def load_image(uploaded_file):
    """Load and process the uploaded image"""
    try:
        # Read the uploaded file
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Convert to RGB
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

def extract_colors(image, num_colors):
    """Extract dominant colors using K-Means"""
    try:
        # Reshape the image to be a list of pixels
        pixels = image.reshape((-1, 3))
        
        # Perform K-Means clustering
        kmeans = KMeans(n_clusters=num_colors, random_state=42)
        kmeans.fit(pixels)
        
        # Get the colors
        colors = kmeans.cluster_centers_.astype(int)
        
        return colors
    except Exception as e:
        st.error(f"Error extracting colors: {e}")
        return None

def create_palette_image(colors):
    """Create an image displaying the color palette"""
    palette = np.zeros((100, 500, 3), dtype=np.uint8)
    step = 500 // len(colors)
    
    for i, color in enumerate(colors):
        palette[:, i*step:(i+1)*step] = color
        
    return palette

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Load and display the image
    image = load_image(uploaded_file)
    if image is not None:
        # Display original image
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Color extraction
        col1, col2 = st.columns([3, 1])
        with col2:
            num_colors = st.slider("Number of colors", min_value=1, max_value=10, value=5)
            extract_button = st.button("Extract Colors")
        
        if extract_button:
            with st.spinner("Extracting colors..."):
                # Extract colors
                colors = extract_colors(image, num_colors)
                if colors is not None:
                    # Create and display palette
                    palette = create_palette_image(colors)
                    st.image(palette, caption="Color Palette", use_container_width=True)
                    
                    # Display RGB values
                    st.write("RGB Values:")
                    for i, color in enumerate(colors, 1):
                        st.write(f"Color {i}: RGB{tuple(color)}")
