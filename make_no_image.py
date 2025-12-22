from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
out_dir = BASE_DIR / "media" / "todo" / "no_image"
out_dir.mkdir(parents=True, exist_ok=True)

out_path = out_dir / "NO-IMAGE.gif"

# 200x200 회색 바탕 GIF 생성
img = Image.new("RGB", (200, 200), color=(230, 230, 230))
draw = ImageDraw.Draw(img)

text = "NO IMAGE"
# 폰트는 시스템마다 다를 수 있어서 기본 폰트로 처리
draw.text((50, 90), text, fill=(80, 80, 80))

img.save(out_path, format="GIF")
print(f"Created: {out_path}")
