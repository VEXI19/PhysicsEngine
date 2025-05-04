import os
from PIL import Image

def is_yellowish(r, g, b, threshold=100):
    return (
        r == 255 and g == 255 and b == 0
    )

def invert_pixel(r, g, b):
    return (255 - r, 255 - g, 255 - b)

def invert_folder_images(folder_path, output_folder=None):
    if output_folder is None:
        output_folder = os.path.join(folder_path, "negatives")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(folder_path, filename)
            image = Image.open(input_path).convert('RGB')
            pixels = image.load()

            width, height = image.size

            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    if r == 0 and g == 0 and b == 255:
                        pixels[x, y] = (0, 0, 225)
                    elif r == 16 and g == 16 and b == 17:
                        pixels[x, y] = (255, 255, 255)
                    else:
                        pixels[x, y] = invert_pixel(r, g, b)

            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{base_name}.png")
            image.save(output_path)
            print(f"Saved: {output_path}")

    print("Done converting all images.")

# Example usage
invert_folder_images("C:\\Users\\Kuba\\Documents\\GitHub\\PhysicsEngine\\Documentation\\Paper\\images\\ds")
