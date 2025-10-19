from PIL import Image
import os

def convert_to_blackwhite(input_path, output_folder):
    """
    Converts PNG to black and white and saves in static/img
    """
    try:
        img = Image.open(input_path).convert("L")  #conversion
        base_name = os.path.basename(input_path)
        name, ext = os.path.splitext(base_name)
        output_filename = f"{name}_blackwhite.png"
        output_path = os.path.join(output_folder, output_filename)

        img.save(output_path)
        return output_filename
    except Exception as e:
        print(f"Błąd podczas konwersji: {e}")
        return None