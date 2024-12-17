import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def load_image(path):
    """Loads an image from the specified path and converts it to RGB."""
    try:
        image = cv2.imread(path)
        if image is None:
            print("Error: Could not load image. Verify the path.")
            return None
        
        # Check image size
        if image.size > 1920 * 1080 * 3:  # Limit to Full HD resolution
            print("Warning: Image too large. Resizing...")
            scale = np.sqrt((1920 * 1080) / (image.shape[0] * image.shape[1]))
            new_height = int(image.shape[0] * scale)
            new_width = int(image.shape[1] * scale)
            image = cv2.resize(image, (new_width, new_height))
            
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def extract_colors(image, num_colors):
    """Extracts dominant colors using K-Means."""
    try:
        pixels = image.reshape((-1, 3))
        kmeans = KMeans(n_clusters=num_colors, random_state=42)
        kmeans.fit(pixels)
        return kmeans.cluster_centers_.astype(int)
    except Exception as e:
        print(f"Error extracting colors: {e}")
        return None

def show_palette(colors):
    """Shows the dominant color palette and their RGB values."""
    if colors is None:
        return
    
    num_colors = len(colors)
    palette = np.zeros((100, 300, 3), dtype='uint8')
    step = 300 // num_colors
    
    plt.figure(figsize=(10, 4))
    
    # Create visual palette
    for i, color in enumerate(colors):
        palette[:, i * step:(i + 1) * step] = color
        
    plt.imshow(palette)
    plt.axis('off')
    
    # Show RGB values
    print("\nRGB values of dominant colors:")
    for i, color in enumerate(colors, 1):
        print(f"Color {i}: RGB{tuple(color)}")
    
    plt.show()

def save_palette(colors, output_path):
    """Saves the color palette as an image."""
    try:
        num_colors = len(colors)
        palette = np.zeros((100, 300, 3), dtype='uint8')
        step = 300 // num_colors
        
        for i, color in enumerate(colors):
            palette[:, i * step:(i + 1) * step] = color
            
        # Convert from RGB to BGR to save with cv2
        palette_bgr = cv2.cvtColor(palette, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, palette_bgr)
        print(f"Palette successfully saved to {output_path}")
        return True
    except Exception as e:
        print(f"Error saving palette: {e}")
        return False

def menu():
    print("\nOptions menu:")
    print("1. Load image")
    print("2. Generate color palette")
    print("3. Save current palette")
    print("4. Exit")

def main():
    image = None
    current_colors = None
    
    while True:
        menu()
        option = input("Select an option: ")
        
        if option == "1":
            path = input("Enter image path: ")
            image = load_image(path)
            if image is not None:
                print("Image successfully loaded.")
                
        elif option == "2":
            if image is None:
                print("You must load an image first.")
                continue
                
            try:
                num_colors = int(input("Enter the number of dominant colors (e.g. 5): "))
                if num_colors <= 0:
                    print("Please enter a number greater than 0.")
                    continue
                    
                current_colors = extract_colors(image, num_colors)
                if current_colors is not None:
                    print("Palette generated. Showing dominant colors...")
                    show_palette(current_colors)
            except ValueError:
                print("Please enter a valid number.")
                
        elif option == "3":
            if current_colors is None:
                print("You must generate a color palette first.")
                continue
                
            output_path = input("Enter path to save palette (e.g. palette.png): ")
            save_palette(current_colors, output_path)
            
        elif option == "4":
            print("Exiting program. Goodbye!")
            break
            
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()