from PIL import Image
import numpy as np

def detect_color(image_field):
    try:
        image = Image.open(image_field)
        image = image.convert('RGB')
        image = image.resize((50, 50))

        np_img = np.array(image)
        avg_color = np.mean(np_img.reshape(-1, 3), axis=0)

        r, g, b = avg_color
        print(f"Average color: R={r:.2f}, G={g:.2f}, B={b:.2f}")

        if g - r < 20 and r > 180:
            return "Negative"
        elif g > 130 and r < 100:
            return "+1"
        elif g > 110 and r < 90:
            return "+2"
        elif g > 90 and r < 80:
            return "+3"
        else:
            return "Unknown"
    except Exception as e:
        print("Color detection failed:", e)
        return "Unknown"
