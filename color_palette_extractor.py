import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def cargar_imagen(ruta):
    """Carga una imagen desde la ruta especificada y la convierte a RGB."""
    try:
        imagen = cv2.imread(ruta)
        if imagen is None:
            print("Error: No se pudo cargar la imagen. Verifica la ruta.")
            return None
        
        # Verificar tamaño de imagen
        if imagen.size > 1920 * 1080 * 3:  # Limitar a resolución Full HD
            print("Advertencia: Imagen muy grande. Redimensionando...")
            scale = np.sqrt((1920 * 1080) / (imagen.shape[0] * imagen.shape[1]))
            nueva_altura = int(imagen.shape[0] * scale)
            nueva_anchura = int(imagen.shape[1] * scale)
            imagen = cv2.resize(imagen, (nueva_anchura, nueva_altura))
            
        return cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        return None

def extraer_colores(imagen, num_colores):
    """Extrae colores dominantes usando K-Means."""
    try:
        pixels = imagen.reshape((-1, 3))
        kmeans = KMeans(n_clusters=num_colores, random_state=42)
        kmeans.fit(pixels)
        return kmeans.cluster_centers_.astype(int)
    except Exception as e:
        print(f"Error al extraer colores: {e}")
        return None

def mostrar_paleta(colores):
    """Muestra la paleta de colores dominantes y sus valores RGB."""
    if colores is None:
        return
    
    num_colores = len(colores)
    palette = np.zeros((100, 300, 3), dtype='uint8')
    step = 300 // num_colores
    
    plt.figure(figsize=(10, 4))
    
    # Crear paleta visual
    for i, color in enumerate(colores):
        palette[:, i * step:(i + 1) * step] = color
        
    plt.imshow(palette)
    plt.axis('off')
    
    # Mostrar valores RGB
    print("\nValores RGB de los colores dominantes:")
    for i, color in enumerate(colores, 1):
        print(f"Color {i}: RGB{tuple(color)}")
    
    plt.show()

def guardar_paleta(colores, ruta_salida):
    """Guarda la paleta de colores como imagen."""
    try:
        num_colores = len(colores)
        palette = np.zeros((100, 300, 3), dtype='uint8')
        step = 300 // num_colores
        
        for i, color in enumerate(colores):
            palette[:, i * step:(i + 1) * step] = color
            
        # Convertir de RGB a BGR para guardar con cv2
        palette_bgr = cv2.cvtColor(palette, cv2.COLOR_RGB2BGR)
        cv2.imwrite(ruta_salida, palette_bgr)
        print(f"Paleta guardada exitosamente en {ruta_salida}")
        return True
    except Exception as e:
        print(f"Error al guardar la paleta: {e}")
        return False

def menu():
    print("\nMenú de opciones:")
    print("1. Cargar imagen")
    print("2. Generar paleta de colores")
    print("3. Guardar paleta actual")
    print("4. Salir")

def main():
    imagen = None
    colores_actuales = None
    
    while True:
        menu()
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            ruta = input("Ingresa la ruta de la imagen: ")
            imagen = cargar_imagen(ruta)
            if imagen is not None:
                print("Imagen cargada exitosamente.")
                
        elif opcion == "2":
            if imagen is None:
                print("Primero debes cargar una imagen.")
                continue
                
            try:
                num_colores = int(input("Ingresa el número de colores dominantes (ej. 5): "))
                if num_colores <= 0:
                    print("Por favor, ingresa un número mayor a 0.")
                    continue
                    
                colores_actuales = extraer_colores(imagen, num_colores)
                if colores_actuales is not None:
                    print("Paleta generada. Mostrando colores dominantes...")
                    mostrar_paleta(colores_actuales)
            except ValueError:
                print("Por favor, ingresa un número válido.")
                
        elif opcion == "3":
            if colores_actuales is None:
                print("Primero debes generar una paleta de colores.")
                continue
                
            ruta_salida = input("Ingresa la ruta para guardar la paleta (ej. paleta.png): ")
            guardar_paleta(colores_actuales, ruta_salida)
            
        elif opcion == "4":
            print("Saliendo del programa. ¡Adiós!")
            break
            
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
