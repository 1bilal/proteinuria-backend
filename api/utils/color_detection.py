import numpy as np
from PIL import Image


def detect_color(image_field):
    """
    Detects the result of a proteinuria test strip by analyzing the dominant color
    of the center of the image in the HSV color space.
    """
    try:
        image = Image.open(image_field)
        image = image.convert("RGB")

        # 1. Center Crop: Focus on the center 50% of the image to avoid background noise
        width, height = image.size
        left = width * 0.25
        top = height * 0.25
        right = width * 0.75
        bottom = height * 0.75
        image = image.crop((left, top, right, bottom))

        # 2. Resize for speed
        image = image.resize((100, 100))

        # 3. Quantize to find dominant colors (reduce to 5 colors)
        # This effectively clusters the pixels
        quantized = image.quantize(colors=5, method=2)  # method=2 is Fast Octree
        palette = quantized.getpalette()[:15]  # Get the top 5 RGB colors (5 * 3 values)
        
        # Convert palette to list of (R, G, B) tuples
        colors = [tuple(palette[i:i+3]) for i in range(0, len(palette), 3)]

        best_color = None
        max_saturation = -1

        print("Dominant colors found (RGB):", colors)

        # 4. Analyze colors in HSV
        for rgb in colors:
            # Convert RGB (0-255) to HSV (0-1, 0-1, 0-255) manually or use colorsys
            # Here we use a simple conversion or just use Pillow's conversion on a 1x1 pixel
            temp_img = Image.new("RGB", (1, 1), rgb)
            hsv_pixel = temp_img.convert("HSV").getpixel((0, 0))
            
            h, s, v = hsv_pixel
            # Pillow HSV: H (0-255), S (0-255), V (0-255)
            
            print(f"Checking Color RGB{rgb} -> HSV(H={h}, S={s}, V={v})")

            # Filter out background (whites, grays, blacks)
            # Low saturation = white/gray
            # Low value = black
            if s < 40 or v < 40:
                continue

            # We want the most "colorful" color that isn't background
            if s > max_saturation:
                max_saturation = s
                best_color = (h, s, v)

        if not best_color:
            print("No valid color found (all appear to be background). Defaulting to Unknown.")
            return "Unknown"

        hue, saturation, value = best_color
        print(f"Selected Best HSV: H={hue}, S={saturation}, V={value}")

        # 5. Map Hue to Result
        # Note: Pillow H is 0-255, mapping 0-360 degrees. 
        # Yellow is ~60 deg -> ~42 in Pillow
        # Green is ~120 deg -> ~85 in Pillow
        
        # Adjusted ranges based on standard urine strip colors
        if 20 <= hue <= 45:
            return "Negative"      # Yellow
        elif 46 <= hue <= 60:
            return "Trace"         # Yellow-Green
        elif 61 <= hue <= 80:
            return "+1"            # Green
        elif 81 <= hue <= 100:
            return "+2"            # Darker Green
        elif 101 <= hue <= 140:
            return "+3"            # Blue-Green / Dark Green
        else:
            return "Unknown"

    except Exception as e:
        print("Color detection failed:", e)
        return "Unknown"
