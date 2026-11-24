import random
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont

class Captcha:

    # Generating Captcha and equation
    def generate_captcha():
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        equation = f"{num1} + {num2} = ?"
        width, height = 80, 20
        image = Image.new("RGB", (width, height), (255, 255, 255))  # Białe tło
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", size=16)
        except IOError:
            font = ImageFont.load_default()
        text_width, text_height = draw.textbbox((0, 6), equation, font=font)[2:]
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2
        draw.text((text_x, text_y), equation, fill=(0, 0, 0), font=font)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        return f"data:image/png;base64,{img_base64}", num1 + num2