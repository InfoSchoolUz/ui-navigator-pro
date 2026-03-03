import base64
from io import BytesIO
from PIL import Image

def pil_to_b64_png(img: Image.Image) -> str:
    bio = BytesIO()
    img.save(bio, format="PNG")
    return base64.b64encode(bio.getvalue()).decode("utf-8")